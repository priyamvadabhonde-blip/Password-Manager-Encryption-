import tkinter as tk
from tkinter import messagebox
import base64
import os

FILE = "passwords.txt"
MASTER_PASSWORD = "admin123"   # change this if you want

# Encrypt
def encrypt(text):
    return base64.b64encode(text.encode()).decode()

# Decrypt
def decrypt(text):
    return base64.b64decode(text.encode()).decode()

# Save password
def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    if website == "" or username == "" or password == "":
        messagebox.showwarning("Error", "All fields required!")
        return

    enc_pass = encrypt(password)

    with open(FILE, "a") as f:
        f.write(f"{website},{username},{enc_pass}\n")

    messagebox.showinfo("Success", "Password Saved!")

    entry_website.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# View passwords
def view_passwords():
    if not os.path.exists(FILE):
        messagebox.showinfo("Info", "No data found!")
        return

    with open(FILE, "r") as f:
        data = f.readlines()

    result = ""
    for line in data:
        website, username, password = line.strip().split(",")
        result += f"{website} | {username} | {decrypt(password)}\n"

    messagebox.showinfo("Saved Passwords", result)

# Login check
def check_login():
    if entry_master.get() == MASTER_PASSWORD:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Wrong Password!")

# Main app window
def open_main_window():
    global entry_website, entry_username, entry_password

    window = tk.Tk()
    window.title("Password Manager")

    tk.Label(window, text="Website").pack()
    entry_website = tk.Entry(window)
    entry_website.pack()

    tk.Label(window, text="Username").pack()
    entry_username = tk.Entry(window)
    entry_username.pack()

    tk.Label(window, text="Password").pack()
    entry_password = tk.Entry(window, show="*")
    entry_password.pack()

    tk.Button(window, text="Save", command=save_password).pack(pady=5)
    tk.Button(window, text="View Passwords", command=view_passwords).pack(pady=5)

    window.mainloop()

# Login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Enter Master Password").pack()
entry_master = tk.Entry(login_window, show="*")
entry_master.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=5)

login_window.mainloop()