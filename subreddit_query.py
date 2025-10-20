import praw
import sys
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
# === Define Search Parameters ===


try:
    reddit = praw.Reddit(
        client_id=config["REDDIT"]["client_id"],
        client_secret=config["REDDIT"]["client_secret"],
        user_agent=config["REDDIT"]["user_agent"],
        username=config["REDDIT"]["username"],
        password=config["REDDIT"]["password"],
    )
    print("Reddit Read-Only Mode:", reddit.read_only)
    print("Logged in as:", reddit.user.me())
except Exception as e:
    print("Reddit API Login Failed:", e)
    sys.exit(1)

    print(reddit.read_only)  # Should return False if authentication is successful
    print(reddit.user.me())
subreddits = ["smartphones", "iphone", "android", "samsung", "technology"]
subreddit_query = reddit.subreddit("+".join(subreddits))

iphone_keywords = ["iPhone", "Apple"]
samsung_keywords = ["Samsung", "Galaxy"]