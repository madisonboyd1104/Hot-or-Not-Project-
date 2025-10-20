import praw
import configparser
import sys
from subreddit_query import subreddits , subreddit_query , iphone_keywords , samsung_keywords

# === Function to Fetch Posts (Titles + Post Content) ===
def fetch_posts(subreddit_query, keywords):
    posts = []
    for keyword in keywords:
        for submission in subreddit_query.search(keyword, limit=10):
            full_text = submission.title + " " + (submission.selftext[:500] if submission.selftext else "")
            posts.append(full_text)
    return posts