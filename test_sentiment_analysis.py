import pytest
from sentiment_analysis import preprocess_text, analyze_sentiment

# -------------------------------
# Test 1: Preprocess text
# -------------------------------
def test_preprocess_text_removes_punctuation_and_lowercases():
    input_text = "Wow! iPhone's Camera, is AMAZING!!!"
    expected_output = "wow iphones camera is amazing"
    assert preprocess_text(input_text) == expected_output


# -------------------------------
# Test 2: Positive sentiment
# -------------------------------
def test_analyze_sentiment_positive_post():
    posts = ["I love my iPhone. It is amazing and flawless."]
    result = analyze_sentiment(posts)
    assert result["positive"] == 1
    assert result["neutral"] == 0
    assert result["negative"] == 0


# -------------------------------
# Test 3: Negative sentiment
# -------------------------------
def test_analyze_sentiment_negative_post():
    posts = ["This phone is terrible and slow, absolute garbage."]
    result = analyze_sentiment(posts)
    assert result["negative"] == 1
    assert result["neutral"] == 0
    assert result["positive"] == 0


# -------------------------------
# Test 4: Neutral sentiment
# -------------------------------
def test_analyze_sentiment_neutral_post():
    posts = ["Battery life and screen quality are average."]
    result = analyze_sentiment(posts)
    assert result["neutral"] == 1
    assert result["positive"] == 0
    assert result["negative"] == 0


# -------------------------------
# Test 5: Mixed sentiment (edge case)
# -------------------------------
def test_analyze_sentiment_mixed_post():
    posts = ["The camera is amazing but the battery life is terrible."]
    result = analyze_sentiment(posts)
    # Positive (amazing = +9), negative (terrible = -9) - roughly balanced, should be neutral
    assert result["neutral"] == 1
    assert result["positive"] == 0
    assert result["negative"] == 0


# -------------------------------
# Test 6: Multiple posts
# -------------------------------
def test_analyze_sentiment_multiple_posts():
    posts = [
        "Love my iPhone!",           # positive
        "Battery life is average.",  # neutral
        "This phone is awful."       # negative
    ]
    result = analyze_sentiment(posts)
    assert result["positive"] == 1
    assert result["neutral"] == 1
    assert result["negative"] == 1
