import tkinter as tk
from tkinter import messagebox

def check_login(username_entry, password_entry, root_callback):
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        login_window.destroy()
        root_callback()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def login_window(root_callback):
    global login_window
    login_window = tk.Tk()
    login_window.title("HotOrNot - Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(login_window, text="Login", 
              command=lambda: check_login(entry_username, entry_password, root_callback)).pack(pady=20)
    
    tk.Label(login_window, text="Default: admin/password", font=("Arial", 8), fg="gray").pack(pady=5)
    login_window.mainloop()
