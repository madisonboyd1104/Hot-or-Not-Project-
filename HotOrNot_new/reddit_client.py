import praw
import sys
import configparser

def init_reddit():
    config = configparser.ConfigParser()
    config.read("config.ini")

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
        return reddit
    except Exception as e:
        print("Reddit API Login Failed:", e)
        sys.exit(1)
