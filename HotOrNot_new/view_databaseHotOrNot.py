import sqlite3
import tkinter as tk
from tkinter import scrolledtext

def view_database():
    # Create the GUI window
    #db_window = tk.Tk()
    db_window = tk.Toplevel()
    db_window.title("HotOrNot - View Database")
    db_window.geometry("800x500")
    
    # Bring window to front on macOS
    db_window.lift()
    db_window.attributes('-topmost', True)
    db_window.after_idle(db_window.attributes, '-topmost', False)

    text_area = scrolledtext.ScrolledText(db_window, wrap=tk.WORD, width=90, height=25)
    text_area.pack(padx=10, pady=10)

    # Connect to database and fetch data
    conn = sqlite3.connect("reddit_sentiment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT platform, content, sentiment FROM posts ORDER BY id DESC")
    rows = cursor.fetchall()

    # Display data
    for row in rows:
        text_area.insert(tk.END, f"Platform: {row[0]}\nContent: {row[1]}\nSentiment: {row[2]}\n{'-'*60}\n")

    conn.close()
    db_window.mainloop()
