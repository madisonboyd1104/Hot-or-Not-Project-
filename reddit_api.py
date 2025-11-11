import praw
import configparser
import sys
from subreddit_query import subreddits , subreddit_query , iphone_keywords , samsung_keywords

# === Function to Fetch Posts (Titles + Post Content) ===
def fetch_posts(subreddit_query, keywords,post_limit = 500):#Jared Johnson
    posts = []#Jared Johnson
    while(len(posts)<post_limit):#Jared Johnson
        for keyword in keywords:#Jared Johnson
            for submission in subreddit_query.search(keyword, limit=10):#Jared Johnson
                full_text = submission.title + " " + (submission.selftext[:500] if submission.selftext else "")#Jared Johnson
                posts.append(full_text)
            
        
    return posts