import sqlite3

def init_db():
    conn = sqlite3.connect("reddit_sentiment.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            content TEXT,
            sentiment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(platform, posts, sentiment_data):
    # conn = sqlite3.connect("reddit_sentiment.db")
    # cursor = conn.cursor()
    # sentiment = "Positive" if sentiment_data['positive'] > sentiment_data['negative'] else (
    #     "Negative" if sentiment_data['negative'] > sentiment_data['positive'] else "Neutral")
    
    # for post in posts:
    #     cursor.execute("INSERT INTO posts (platform, content, sentiment) VALUES (?, ?, ?)", 
    #                    (platform, post, sentiment))
    # conn.commit()
    # conn.close()

    conn_local = sqlite3.connect("reddit_sentiment.db")
    cursor_local = conn_local.cursor()
    for post in posts:
        sentiment = "Positive" if sentiment_data['positive'] > sentiment_data['negative'] else ("Negative" if sentiment_data['negative'] > sentiment_data['positive'] else "Neutral")
        cursor_local.execute("INSERT INTO posts (platform, content, sentiment) VALUES (?, ?, ?)", (platform, post, sentiment))
    conn_local.commit()
    conn_local.close()
