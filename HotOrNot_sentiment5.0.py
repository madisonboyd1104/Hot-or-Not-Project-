import praw  # Python Reddit API Wrapper
import re
import sqlite3
from view_databaseHotOrNot import view_database
import sys
from collections import Counter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext

# Configure matplotlib backend before importing pyplot
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better macOS compatibility
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import configparser

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
except Exception as e:
    print("Reddit API Login Failed:", e)
    sys.exit(1)

print(reddit.read_only)  # Should return False if authentication is successful
print(reddit.user.me())

# === Initialize SQLite Database ===
conn = sqlite3.connect("reddit_sentiment.db")
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        content TEXT,
        sentiment TEXT
    )
''')
conn.commit()

def check_login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Simple authentication (replace with a secure method as needed)
    if username == "admin" and password == "password":
        login_window.destroy()
        create_gui()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create login window
login_window = tk.Tk()
login_window.title("HotOrNot - Login")
login_window.geometry("300x200")

# Bring window to front on macOS
login_window.lift()
login_window.attributes('-topmost', True)
login_window.after_idle(login_window.attributes, '-topmost', False)

tk.Label(login_window, text="Username:").pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

tk.Label(login_window, text="Password:").pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

tk.Button(login_window, text="Login", command=check_login).pack(pady=20)

# Add instructions
tk.Label(login_window, text="Default: admin/password", font=("Arial", 8), fg="gray").pack(pady=5)

print("Login window created. Please check your screen for the login window.")
login_window.mainloop()

# === New Sentiment Dictionary (Scale: -10 to 10) ===
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


# === Define Search Parameters ===
subreddits = ["smartphones", "iphone", "android", "samsung", "technology"]
subreddit_query = reddit.subreddit("+".join(subreddits))

iphone_keywords = ["iPhone", "Apple"]
samsung_keywords = ["Samsung", "Galaxy"]

# === Function to Fetch Posts (Titles + Post Content) ===
def fetch_posts(subreddit_query, keywords):
    posts = []
    for keyword in keywords:
        for submission in subreddit_query.search(keyword, limit=10):
            full_text = submission.title + " " + (submission.selftext[:500] if submission.selftext else "")
            posts.append(full_text)
    return posts

# === Function to Save Posts to Database ===
def save_to_db(platform, posts, sentiment_data):
    conn_local = sqlite3.connect("reddit_sentiment.db")
    cursor_local = conn_local.cursor()
    for post in posts:
        sentiment = "Positive" if sentiment_data['positive'] > sentiment_data['negative'] else ("Negative" if sentiment_data['negative'] > sentiment_data['positive'] else "Neutral")
        cursor_local.execute("INSERT INTO posts (platform, content, sentiment) VALUES (?, ?, ?)", (platform, post, sentiment))
    conn_local.commit()
    conn_local.close()

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


def plot_pie_chart(sentiment_data, title):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiment_data['positive'], sentiment_data['neutral'], sentiment_data['negative']]
    colors = ['green', 'gray', 'red']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title(title)
    ax.set_aspect('equal')
    return fig

def on_closing():
    """Ensures program exits when GUI is closed."""
    print("Closing GUI...")
    root.destroy()
    sys.exit()  # Forces the program to stop running

def show_analysis(selection):
    fig = None

    if selection == "iPhone Posts":
        posts = fetch_posts(subreddit_query, iphone_keywords)
        sentiment_counts = analyze_sentiment(posts)
        fig = plot_pie_chart(sentiment_counts, "Sentiment Analysis for iPhone")
    elif selection == "Samsung Posts":
        posts = fetch_posts(subreddit_query, samsung_keywords)
        sentiment_counts = analyze_sentiment(posts)
        fig = plot_pie_chart(sentiment_counts, "Sentiment Analysis for Samsung")
    elif selection == "Compare Both":
        iphone_posts = fetch_posts(subreddit_query, iphone_keywords)
        samsung_posts = fetch_posts(subreddit_query, samsung_keywords)
        iphone_sentiments = analyze_sentiment(iphone_posts)
        samsung_sentiments = analyze_sentiment(samsung_posts)
        
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].pie(iphone_sentiments.values(), labels=iphone_sentiments.keys(), autopct='%1.1f%%', colors=['green', 'red', 'gray'])
        axes[0].set_title("iPhone Sentiment")
        axes[1].pie(samsung_sentiments.values(), labels=samsung_sentiments.keys(), autopct='%1.1f%%', colors=['blue', 'red', 'gray'])
        axes[1].set_title("Samsung Sentiment")
    else:
        print("Invalid selection received:", selection)
        return  # Exit the function early
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def create_gui():
    global root, frame 
    root = tk.Tk()
    root.title("HotOrNot - Reddit Sentiment Analysis")
    root.geometry("800x600")
    
    # Bring window to front on macOS
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handles closing event

    # Main Title
    tk.Label(root, text="HotOrNot Sentiment Analyzer", font=("Arial", 24, "bold"), 
             bg="light blue", fg="black").pack(pady=(20, 5))

    # Subtitle
    tk.Label(root, text="iPhone vs. Samsung, who comes out on top?", font=("Arial", 16), 
             bg="light blue", fg="black").pack(pady=(0, 20))

    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=["iPhone Posts", "Samsung Posts", "Compare Both"])
    dropdown.pack(pady=10)
    dropdown.current(0)  # Optional: Set default selection


    tk.Button(root, text="Analyze", command=lambda: show_analysis(dropdown_var.get())).pack(pady=10)
   
    btn_view_ns=tk.Button(root,text="Post With No Sentiment", command=fetch_no_sentiment_posts)
    btn_view_ns.place(relx=1.0, y=70, x=-150, anchor="nw")
    # Button to View Database
    btn_view_db = tk.Button(root, text="View Database", command=view_database)
    btn_view_db.place(relx=1.0, y=10, x=-10, anchor="ne") 

    frame = tk.Frame(root, bg = "light blue")
    frame.pack(fill = "both", expand = True)

    root.mainloop()

create_gui() 










