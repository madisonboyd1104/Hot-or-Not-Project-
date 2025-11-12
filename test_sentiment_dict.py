# -----------------------------------
# Test file created By David Jackson 
# -----------------------------------

import pytest
from sentiment_dict import preprocess_text, analyze_sentiment, analyze_sentiment_dictionary, sentiment_dict


# -----------------------------------
# TESTS FOR preprocess_text
# -----------------------------------

# Tests for removing punctuation and converting to lowercase
def test_preprocess_text_removes_punctuation():
    text = "Amazing, product!!! Works perfectly."
    expected = "amazing product works perfectly"
    assert preprocess_text(text) == expected

# Test for lowercase conversion
def test_preprocess_text_lowercase_conversion():
    text = "ThIs Is A TeSt"
    expected = "this is a test"
    assert preprocess_text(text) == expected


# -----------------------------------
# TESTS FOR BERT-BASED analyze_sentiment
# -----------------------------------

def test_analyze_sentiment_with_mock(mocker):
    """Mock BERT-based analyze_sentiment_bert to ensure correct integration."""
    mock_func = mocker.patch("sentiment_dict.analyze_sentiment_bert", return_value={"positive": 2, "neutral": 1, "negative": 0})
    posts = ["This phone is amazing!", "Battery life is fine", "No major issues"]
    result = analyze_sentiment(posts)
    mock_func.assert_called_once_with(posts)
    assert result == {"positive": 2, "neutral": 1, "negative": 0}


# -----------------------------------
# TESTS FOR dictionary-BASED analyze_sentiment
# -----------------------------------

# Tests for positive sentiment analysis
def test_analyze_sentiment_positive(mocker):
    """Force dictionary-based analysis to avoid BERT dependency."""
    mocker.patch("sentiment_dict.analyze_sentiment_bert", side_effect=Exception("BERT disabled"))
    posts = ["This phone is amazing and perfect", "I love how fast and smooth it feels"]
    result = analyze_sentiment(posts)
    assert result["positive"] > 0
    assert result["negative"] == 0

# Tests for negative sentiment analysis
def test_analyze_sentiment_negative(mocker):
    """Force dictionary-based analysis to avoid BERT dependency."""
    mocker.patch("sentiment_dict.analyze_sentiment_bert", side_effect=Exception("BERT disabled"))
    posts = ["This phone is terrible and slow", "I hate the laggy interface"]
    result = analyze_sentiment(posts)
    assert result["negative"] > 0
    assert result["positive"] == 0

# Tests for neutral sentiment analysis
def test_analyze_sentiment_neutral(mocker):
    """Force dictionary-based analysis to avoid BERT dependency."""
    mocker.patch("sentiment_dict.analyze_sentiment_bert", side_effect=Exception("BERT disabled"))
    posts = ["This phone has a display and a battery", "The screen and design are fine"]
    result = analyze_sentiment(posts)
    assert result["neutral"] > 0

# Tests for mixed sentiment analysis
def test_analyze_sentiment_mixed(mocker):
    """Force dictionary-based analysis to avoid BERT dependency."""
    mocker.patch("sentiment_dict.analyze_sentiment_bert", side_effect=Exception("BERT disabled"))
    posts = ["The camera is good but the battery life is terrible"]
    result = analyze_sentiment(posts)
    # Should count as mixed, but classified based on score balance
    assert result["positive"] + result["negative"] + result["neutral"] == 1

# Tests for empty list input
def test_analyze_sentiment_empty_list(mocker):
    """Force dictionary-based analysis to avoid BERT dependency."""
    mocker.patch("sentiment_dict.analyze_sentiment_bert", side_effect=Exception("BERT disabled"))
    result = analyze_sentiment([])
    assert result == {"positive": 0, "neutral": 0, "negative": 0}


# -----------------------------------
# TESTS FOR SENTIMENT DICTIONARY
# -----------------------------------

# Tests for accurate sentiment dictionary contents
def test_sentiment_dict_contains_expected_words():
    assert "love" in sentiment_dict
    assert "hate" in sentiment_dict
    assert sentiment_dict["love"] > 0
    assert sentiment_dict["hate"] < 0
