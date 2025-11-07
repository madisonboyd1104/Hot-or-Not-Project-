"""
This is the bert_sentiment.py file

This performs a sentiment analysis using a BERT model that's pre-trained.

This new approach replaces the old dictionary-based approach. This new approach has a
model that's aware of the context of the posts. It also understands tone and sarcasm as
well as how a word is phrased. It also predicts a 1-5 star rating and then it's converted
into either a positive or negative sentiment.

"""

from transformers import pipeline
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Initialize BERT sentiment analysis pipeline
print("Initializing BERT sentiment model...")
print("Note: First run will download ~500MB model (cached for future use)")


#This loads the BERT model when this module is imported.
#The output is a 1-5 star rating that will be converted to a sentiment.
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        truncation=True,
        max_length=512
    )
    print("✓ BERT model loaded successfully!")
except Exception as e:
    print(f"Error loading BERT model: {e}")
    print("Falling back to dictionary-based analysis...")
    sentiment_pipeline = None


def analyze_sentiment_bert(posts):
    """
    This analyzes the sentiment based on a list of text from the posts. 
    
    Args:
        posts (list): Reddit posts 
    
    Returns:
        dict: Sentiment dictionary with counts - {"positive": int, "negative": int}

    Purpose:
        - Counts the number of occurrences of a word from the lists.
        - Classifies the overall sentiment based on the count with the largest amount.
    """
    sentiments = {"positive": 0, "negative": 0}
    
    if sentiment_pipeline is None:
        print("BERT model not available. Please install transformers and torch.")
        return sentiments
    
    for post in posts:
        # This handles empty posts by skipping empty/blank posts
        if not post or not post.strip():
            continue
        
        try:
            # This shortens posts that are long so that it avoids processing issues
            text_sample = post[:500] if len(post) > 500 else post
            
            # This gets the BERT prediction
            result = sentiment_pipeline(text_sample)[0]
            label = result['label']  # Format: "1 star", "2 stars", etc.
            
            # This gets the star rating and then converts it to sentiment
            # Model outputs: 1 star (very negative) to 5 stars (very positive)
            stars = int(label.split()[0])
            
            if stars <= 3:
                sentiments["negative"] += 1
            else:  # stars >= 4
                sentiments["positive"] += 1
                
        except Exception as e:
            print(f"Error analyzing post: {e}")
            # This defaults to neutral on error
            sentiments["negative"] += 1
    
    return sentiments


def get_sentiment_with_confidence(text):
    """
    This analyzes an individual post and them returns the sentiment, confidence, and star rating.
    
    This will help provide a more detailed output and this will be useful when we need to debug or test things.
    This will also help with future enhancements if needed.
    
    Args:
        text (str): The input text that's being analyzed
    
    Returns:
        dict: This contains the model's prediction in the following format: 
            {
                "sentiment": "positive" | "negative",
                "confidence":   #this is the model's confidence score (0-1)
                "stars": int    #this is the star rating from BERT (1-5)
            }
    """
    if sentiment_pipeline is None:
        return {"sentiment": "negative", "confidence": 0.0, "stars": 3}
    
    try:
        text_sample = text[:500] if len(text) > 500 else text
        result = sentiment_pipeline(text_sample)[0]
        
        stars = int(result['label'].split()[0])
        confidence = result['score']
        
        #removed the "neutral sentiment" sinces it's redundant 
        if stars <= 3:
            sentiment = "negative"
        else:
            sentiment = "positive"
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "stars": stars
        }
    except Exception as e:
        #This will just return a negative result if there's an error.  
        print(f"Error in detailed analysis: {e}")
        return {"sentiment": "negative", "confidence": 0.0, "stars": 3}

