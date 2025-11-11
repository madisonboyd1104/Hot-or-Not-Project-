# BERT Integration - Implementation Notes

## What Changed

### 1. New File: `bert_sentiment.py`
- **Purpose**: BERT-based sentiment analysis using transformers
- **Model**: `nlptown/bert-base-multilingual-uncased-sentiment`
- **Key Function**: `analyze_sentiment_bert(posts)` 
  - Returns same format as dictionary method: `{"positive": N, "neutral": N, "negative": N}`
  - Maps 1-2 stars → Negative, 3 stars → Neutral, 4-5 stars → Positive
- **Bonus Function**: `get_sentiment_with_confidence(text)` for detailed analysis (future use)

### 2. Updated: `requirements.txt`
Added:
- `transformers>=4.30.0` - HuggingFace library for BERT
- `torch>=2.0.0` - PyTorch backend

### 3. Updated: `sentiment_dict.py`
- **Main Change**: `analyze_sentiment()` now calls `analyze_sentiment_bert()` instead of dictionary logic
- **Preserved**: Old dictionary-based method renamed to `analyze_sentiment_dictionary()` for reference
- **Dictionary**: Retained in code for future experimentation/fallback

## How to Use

### First Time Setup
```bash
# Install new dependencies (from project root)
pip install -r requirements.txt
```

**Note**: First run will download ~500MB BERT model (one-time, cached locally)

### Running the Application
No changes needed! Run as normal:
```bash
python main.py
# or
python HotOrNot_sentiment5.0.py
```

The GUI and all existing functionality work exactly the same, but now use BERT for sentiment analysis.

## Benefits Over Dictionary Method

1. **Context-Aware**: Understands phrases and context, not just individual words
2. **Sarcasm Detection**: Better at detecting sarcastic/ironic statements
3. **Multilingual**: Works with multiple languages (helpful for international posts)
4. **No Manual Updates**: No need to manually add slang/new terms to dictionary
5. **Semantic Understanding**: Captures meaning beyond keyword matching

## Technical Details

### Import Chain
```
GUI_build.py 
  → imports analyze_sentiment from sentiment_dict.py
    → calls analyze_sentiment_bert from bert_sentiment.py
      → uses HuggingFace transformers pipeline
```

### Error Handling
- Gracefully handles model loading failures
- Falls back to neutral classification on individual post errors
- Truncates very long posts to 500 chars to avoid processing issues

## Future Enhancements

You can easily modify/extend:
1. Change star-to-sentiment mapping in `bert_sentiment.py`
2. Use `get_sentiment_with_confidence()` to show confidence scores in GUI
3. Switch back to dictionary method by changing the import in `sentiment_dict.py`
4. Try different BERT models by changing the model name in `bert_sentiment.py`
5. Add A/B comparison between BERT and dictionary methods

## Switching Back to Dictionary (if needed)

In `sentiment_dict.py`, change:
```python
def analyze_sentiment(posts):
    return analyze_sentiment_bert(posts)
```
To:
```python
def analyze_sentiment(posts):
    return analyze_sentiment_dictionary(posts)
```

## Model Information

- **Model**: nlptown/bert-base-multilingual-uncased-sentiment
- **Size**: ~500MB
- **Languages**: 6 languages (English, Dutch, German, French, Spanish, Italian)
- **Training**: Fine-tuned on product reviews
- **Output**: 5-star rating system (1-5 stars)
- **Cache Location**: `~/.cache/huggingface/` (default)

## Performance Notes

- BERT is slower than dictionary (~0.1-0.5s per post vs instant)
- For 20-30 posts, total analysis time is 2-10 seconds
- Model loads once at startup, then cached in memory
- First run requires internet to download model
- Subsequent runs work offline with cached model

