from reddit_client import init_reddit
from database_utils import init_db
from login import login_window
from gui import create_gui

def main():
    init_db()
    reddit = init_reddit()
    login_window(lambda: create_gui(reddit))

if __name__ == "__main__":
    main()