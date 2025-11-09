import re
from subreddit_query import subreddits , subreddit_query , iphone_keywords , samsung_keywords
# === New Sentiment Dictionary (Scale: -10 to 10) ===
# === Define Search Parameters ===

sentiment_dict = {

    # Strongly Positive (8-10)
    "love": 10, "best": 9, "amazing": 9, "excellent": 9, "superior": 9, "outstanding": 9, "phenomenal": 9,
    "incredible": 9, "fantastic": 9, "brilliant": 9, "perfect": 9, "game-changer": 9, "exceptional": 9,
    "dope": 9, "lit": 9, "fire": 9, "next-level": 9, "unmatched": 9, "goated": 9, "legendary": 9, 
    "insane": 9, "mind-blowing": 9, "jaw-dropping": 9, "masterpiece": 9, "flawless": 9, "unbeatable": 9,
    "out-of-this-world": 9, "pristine": 9, "stunning": 9, "epic": 9, "top-tier": 9, "10/10": 10,
    
    # Moderately Positive (5-7)
    "great": 7, "happy": 7, "good": 7, "satisfied": 7, "solid": 6, "reliable": 6, "impressive": 6,
    "innovative": 6, "user-friendly": 6, "affordable": 6, "secure": 6, "fast": 6, "smooth": 6, "efficient": 6,
    "valuable": 6, "responsive": 6, "optimized": 6, "enhanced": 6, "long-lasting": 6, "intuitive": 6,
    "clean": 6, "easy-to-use": 6, "handy": 6, "polished": 6, "solid build": 6, "worth it": 6,
    "bang for the buck": 6, "hyped": 6, "trustworthy": 6, "cool": 6, "legit": 6, "straightforward": 6,
    
    # Slightly Positive (1-4)
    "decent": 4, "like": 3, "useful": 3, "okay": 3, "acceptable": 3, "fine": 3, "works": 3,
    "lightweight": 3, "handy": 3, "fair": 3, "standard": 3, "adequate": 3, "improving": 3, "updated": 3,
    "functional": 3, "meh": 3, "not bad": 3, "alright": 3, "does the job": 3, "workable": 3,
    "getting better": 3, "somewhat helpful": 3, "basic but fine": 3,
    
    # Neutral (0)
    "average": 0, "battery life": 0, "storage": 0, "performance": 0, "updates": 0, "price": 0,
    "processor": 0, "display": 0, "camera": 0, "screen": 0, "technology": 0, "resolution": 0, "features": 0,
    "specs": 0, "design": 0, "brand": 0, "interface": 0, "UI": 0, "hardware": 0, "software": 0,
    
    # Slightly Negative (-1 to -4)
    "issue": -1, "problem": -2, "expensive": -3, "slow": -3, "complicated": -3, "lacking": -3,
    "overpriced": -4, "heating": -4, "battery drain": -4, "basic": -3, "underwhelming": -3, "downgrade": -4,
    "not great": -3, "kind of bad": -3, "meh quality": -3, "missing features": -3, "iffy": -3,
    "mid": -3, "sus": -3, "kinda trash": -4, "bug": -3, "cheap feel": -3, "gimmicky": -4,
    
    # Moderately Negative (-5 to -7)
    "buggy": -6, "glitchy": -6, "annoying": -6, "unreliable": -6, "laggy": -6, "frustrating": -6,
    "poor": -6, "disappointed": -7, "dislike": -7, "missing": -6, "short-lived": -6, "outdated": -6,
    "downgraded": -6, "clunky": -6, "underperforming": -6, "difficult": -5, "cheap build": -6,
    "overhyped": -6, "low quality": -6, "too expensive": -6, "lost": -6, "barely functional": -7, "mid-tier": -6,
    "janky": -6, "subpar": -6, "problematic": -6, "bad optimization": -6, "decline": -6,
    
    # Strongly Negative (-8 to -10)
    "hate": -10, "worst": -9, "warns": -9, "awful": -9, "terrible": -9, "horrible": -9, "disaster": -9,
    "scam": -9, "ripoff": -9, "useless": -9, "garbage": -9, "crashes": -9, "dead": -9, "broken": -9,
    "insecure": -9, "failing": -9, "nightmare": -9, "major flaw": -9, "flop": -9, "severe": -9, "completely useless": -10,
    "trash": -9, "hot garbage": -9, "dumpster fire": -9, "straight up bad": -9, "painful to use": -9,
    "refund": -9, "useless junk": -9, "bricked": -9, "unusable": -9, "not worth a penny": -9,
    "total mess": -9, "garbage tier": -9, "beyond repair": -9, "refund ASAP": -9, "never again": -9,
    "absolutely horrendous": -9, "burn it": -10, "0/10": -10
}

# === Function to Clean Text ===
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    return text

def fetch_no_sentiment_posts():
    keywords = iphone_keywords + samsung_keywords
    all_posts = fetch_posts(subreddit_query, keywords)

    no_sentiment_posts = []
    for post in all_posts:
        words = preprocess_text(post).split()
        if all(word not in sentiment_dict for word in words):
            no_sentiment_posts.append(post)

    if not no_sentiment_posts:
        messagebox.showinfo("No Sentiment", "No posts found without sentiment keywords.")
        return

    # Create popup window
    popup = tk.Toplevel(root)
    popup.title("HotOrNot - No Sentiment Posts")
    popup.geometry("700x500")
    
    # Bring window to front on macOS
    popup.lift()
    popup.attributes('-topmost', True)
    popup.after_idle(popup.attributes, '-topmost', False)

    tk.Label(popup, text="Posts Without Sentiment Keywords", font=("Arial", 16, "bold")).pack(pady=10)

    scroll = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=80, height=25)
    scroll.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for idx, post in enumerate(no_sentiment_posts, start=1):
        scroll.insert(tk.END, f"{idx}. {post}\n\n")

    scroll.config(state=tk.DISABLED)


# === Dictionary-Based Sentiment Analysis Function 
def analyze_sentiment(posts):
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    for post in posts:
        words = preprocess_text(post).split()

        # Dictionary-based score
        dict_score = sum(sentiment_dict.get(word, 0) for word in words)

        # Classify sentiment based on the final score
        if dict_score > 1:  # Adjust this threshold as needed
            sentiments["positive"] += 1
        elif dict_score < -1:  # Adjust this threshold as needed
            sentiments["negative"] += 1
        else:
            sentiments["neutral"] += 1

    return sentiments
