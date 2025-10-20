import tkinter as tk
from subreddit_query import subreddits , subreddit_query , iphone_keywords , samsung_keywords
from tkinter import scrolledtext
import sys
import praw
from tkinter import ttk
from reddit_api import fetch_posts
from sentiment_dict import analyze_sentiment
from sentiment_dict import fetch_no_sentiment_posts
from view_databaseHotOrNot import view_database
from db_unit import save_to_db
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better macOS compatibility
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def on_closing():
    """Ensures program exits when GUI is closed."""
    print("Closing GUI...")
    root.destroy()
    sys.exit()  # Forces the program to stop running
def plot_pie_chart(sentiment_data, title):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiment_data['positive'], sentiment_data['neutral'], sentiment_data['negative']]
    colors = ['green', 'gray', 'red']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title(title)
    ax.set_aspect('equal')
    return fig

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












create_gui() 
