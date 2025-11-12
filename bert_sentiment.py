"""
BERT-based Sentiment Analysis Module
Uses pre-trained transformer model for context-aware sentiment classification
"""

import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Initialize BERT sentiment analysis pipeline
sentiment_pipeline = None

try:
    from transformers import pipeline
    
    print("Initializing BERT sentiment model...")
    print("Note: First run will download ~500MB model (cached for future use)")
    
    # Load pre-trained multilingual sentiment model
    # This model outputs 1-5 star ratings which we'll convert to sentiment
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        truncation=True,
        max_length=512
    )
    print("✓ BERT model loaded successfully!")
except ImportError:
    print("⚠️  BERT module not available (transformers package not installed)")
    print("→  Install with: venv/bin/pip install transformers torch")
    print("→  Falling back to dictionary-based sentiment analysis...")
except Exception as e:
    print(f"⚠️  Error loading BERT model: {e}")
    print("→  Falling back to dictionary-based sentiment analysis...")
    sentiment_pipeline = None


def analyze_sentiment_bert(posts):
    """
    Analyze sentiment of Reddit posts using BERT transformer model.
    
    Args:
        posts (list): List of text strings to analyze
    
    Returns:
        dict: Dictionary with counts - {"positive": int, "neutral": int, "negative": int}
    """
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    
    if sentiment_pipeline is None:
        print("BERT model not available. Please install transformers and torch.")
        return sentiments
    
    for post in posts:
        # Handle empty posts
        if not post or not post.strip():
            sentiments["neutral"] += 1
            continue
        
        try:
            # Truncate very long posts to avoid processing issues
            text_sample = post[:500] if len(post) > 500 else post
            
            # Get BERT prediction
            result = sentiment_pipeline(text_sample)[0]
            label = result['label']  # Format: "1 star", "2 stars", etc.
            
            # Extract star rating and convert to sentiment
            # Model outputs: 1 star (very negative) to 5 stars (very positive)
            stars = int(label.split()[0])
            
            if stars <= 2:
                sentiments["negative"] += 1
            elif stars == 3:
                sentiments["neutral"] += 1
            else:  # stars >= 4
                sentiments["positive"] += 1
                
        except Exception as e:
            print(f"Error analyzing post: {e}")
            # Default to neutral on error
            sentiments["neutral"] += 1
    
    return sentiments


def get_sentiment_with_confidence(text):
    """
    Get detailed sentiment analysis with confidence scores.
    Useful for future enhancements and debugging.
    
    Args:
        text (str): Text to analyze
    
    Returns:
        dict: Contains 'sentiment', 'confidence', 'stars'
    """
    if sentiment_pipeline is None:
        return {"sentiment": "neutral", "confidence": 0.0, "stars": 3}
    
    try:
        text_sample = text[:500] if len(text) > 500 else text
        result = sentiment_pipeline(text_sample)[0]
        
        stars = int(result['label'].split()[0])
        confidence = result['score']
        
        if stars <= 2:
            sentiment = "negative"
        elif stars == 3:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "stars": stars
        }
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
        return {"sentiment": "neutral", "confidence": 0.0, "stars": 3}

