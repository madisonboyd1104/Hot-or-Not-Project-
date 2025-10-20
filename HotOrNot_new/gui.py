import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sentiment_analysis import analyze_sentiment, preprocess_text, sentiment_dict
from database_utils import save_to_db
from view_databaseHotOrNot import view_database
#rname the file to gui.py



def fetch_posts(subreddit_query, keywords):
    posts = []
    for keyword in keywords:
        for submission in subreddit_query.search(keyword, limit=10):
            full_text = submission.title + " " + (submission.selftext[:500] if submission.selftext else "")
            posts.append(full_text)
    return posts

def fetch_no_sentiment_posts(root, subreddit_query, iphone_keywords, samsung_keywords):
    from sentiment_analysis import preprocess_text, sentiment_dict
    keywords = iphone_keywords + samsung_keywords
    all_posts = fetch_posts(subreddit_query, keywords)
    no_sentiment_posts = [p for p in all_posts if all(w not in sentiment_dict for w in preprocess_text(p).split())]

    if not no_sentiment_posts:
        messagebox.showinfo("No Sentiment", "No posts found without sentiment keywords.")
        return

    popup = tk.Toplevel(root)
    popup.title("HotOrNot - No Sentiment Posts")
    popup.geometry("700x500")

    tk.Label(popup, text="Posts Without Sentiment Keywords", font=("Arial", 16, "bold")).pack(pady=10)
    scroll = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=80, height=25)
    scroll.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    for i, post in enumerate(no_sentiment_posts, 1):
        scroll.insert(tk.END, f"{i}. {post}\n\n")
    scroll.config(state=tk.DISABLED)

def plot_pie(sentiment_data, title):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiment_data['positive'], sentiment_data['neutral'], sentiment_data['negative']]
    colors = ['green', 'gray', 'red']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title(title)
    ax.axis('equal')
    return fig

def create_gui(reddit):
    root = tk.Tk()
    root.title("HotOrNot - Reddit Sentiment Analysis")
    root.geometry("800x600")

    subreddits = ["smartphones", "iphone", "android", "samsung", "technology"]
    subreddit_query = reddit.subreddit("+".join(subreddits))
    iphone_keywords = ["iPhone", "Apple"]
    samsung_keywords = ["Samsung", "Galaxy"]

    frame = tk.Frame(root, bg="light blue")
    frame.pack(fill="both", expand=True)

    def show_analysis(choice):
        if choice == "iPhone Posts":
            posts = fetch_posts(subreddit_query, iphone_keywords)
            data = analyze_sentiment(posts)
            save_to_db("iPhone", posts, data)
            fig = plot_pie(data, "iPhone Sentiment")
        elif choice == "Samsung Posts":
            posts = fetch_posts(subreddit_query, samsung_keywords)
            data = analyze_sentiment(posts)
            save_to_db("Samsung", posts, data)
            fig = plot_pie(data, "Samsung Sentiment")
        else:
            posts = fetch_posts(subreddit_query, iphone_keywords)
            posts = fetch_posts(subreddit_query, samsung_keywords)
            iphone_data = analyze_sentiment(fetch_posts(subreddit_query, iphone_keywords))
            samsung_data = analyze_sentiment(fetch_posts(subreddit_query, samsung_keywords))
            save_to_db("iPhone", posts, iphone_data)
            save_to_db("Samsung", posts, samsung_data)
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            axes[0].pie(iphone_data.values(), labels=iphone_data.keys(), autopct='%1.1f%%', colors=['green', 'gray', 'red'])
            axes[0].set_title("iPhone")
            axes[1].pie(samsung_data.values(), labels=samsung_data.keys(), autopct='%1.1f%%', colors=['blue', 'gray', 'red'])
            axes[1].set_title("Samsung")

        for widget in frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    tk.Label(root, text="HotOrNot Sentiment Analyzer", font=("Arial", 24, "bold"), bg="light blue").pack(pady=10)
    dropdown = ttk.Combobox(root, values=["iPhone Posts", "Samsung Posts", "Compare Both"])
    dropdown.pack(pady=10)
    dropdown.current(0)
    tk.Button(root, text="Analyze", command=lambda: show_analysis(dropdown.get())).pack(pady=5)
    tk.Button(root, text="View Database", command=view_database).pack(pady=5)
    tk.Button(root, text="Posts Without Sentiment", 
              command=lambda: fetch_no_sentiment_posts(root, subreddit_query, iphone_keywords, samsung_keywords)).pack(pady=5)

    root.mainloop()
