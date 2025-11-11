from view_databaseHotOrNot import view_database
from subreddit_query import reddit
from db_unit import build_db
from GUI_build import create_gui
import configparser

def main():
    print("Starting HotOrNot Sentiment Analyzer...")
    # Reddit connection is already handled in subreddit_query.py
    # Initialize database
    build_db()
    # Launch GUI
    create_gui(reddit)

if __name__ == "__main__":
    main()












