
from view_databaseHotOrNot import view_database
from subreddit_query import reddit
from db_unit import build_db
from GUI_build import create_gui
import configparser
def main():
    print("Starting HotOrNot Sentiment Analyzer...")
    reddit = connect_reddit()# connect to Reddit
    init_db()# ensure database exists
    create_gui(reddit)# launch GUI












