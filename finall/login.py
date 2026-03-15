import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import bcrypt
from db import get_connection

# ------------------ APP PATH ------------------

app_path = r"C:\Users\ASUS\Desktop\finall\app.py"  # change if needed

# ------------------ MAIN WINDOW ------------------

root = tk.Tk()
root.title("Login System")
root.geometry("700x500")
root.minsize(500, 400)

# ------------------ CANVAS (RESPONSIVE BACKGROUND) ------------------

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw_gradient(canvas, width, height, color1, color2):
    canvas.delete("gradient")
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)

    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}"
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")

def on_resize(event):
    draw_gradient(canvas, event.width, event.height, "#4facfe", "#8f00ff")

canvas.bind("<Configure>", on_resize)

# ------------------ CENTER CARD ------------------

card = tk.Frame(canvas, bg="white", width=340, height=360)
card.place(relx=0.5, rely=0.5, anchor="center")

# ------------------ VARIABLES ------------------

mode = tk.StringVar(value="login")

# ------------------ DATABASE FUNCTIONS ------------------

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user["id"]
    return None

# ------------------ FUNCTIONS ------------------

def switch_mode():
    if mode.get() == "login":
        mode.set("register")
        title_label.config(text="Register")

        confirm_label.pack(after=password_entry, fill="x", padx=30)
        confirm_entry.pack(after=confirm_label, padx=30, pady=6, fill="x")

        action_btn.config(text="REGISTER")
        switch_btn.config(text="Already a member? Login")
    else:
        mode.set("login")
        title_label.config(text="Login")

        confirm_label.pack_forget()
        confirm_entry.pack_forget()

        action_btn.config(text="LOGIN")
        switch_btn.config(text="Not a member? Signup now")

def submit():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    # -------- REGISTER --------
    if mode.get() == "register":
        confirm_pwd = confirm_entry.get().strip()

        if password != confirm_pwd:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            switch_mode()
        else:
            messagebox.showerror("Error", "Username already exists")

    # -------- LOGIN --------
    else:
        user_id = login_user(username, password)

        if user_id:
            messagebox.showinfo("Success", f"Welcome {username}!")
            root.destroy()

            subprocess.Popen(
                [sys.executable, app_path, str(user_id), username],
                shell=True
            )
        else:
            messagebox.showerror("Error", "Invalid username or password")

# ------------------ CARD CONTENT ------------------

title_label = tk.Label(card, text="Login", font=("Arial", 18, "bold"), bg="white")
title_label.pack(pady=20)

tk.Label(card, text="Username", bg="white", anchor="w").pack(fill="x", padx=30)
username_entry = tk.Entry(card, font=("Arial", 11))
username_entry.pack(padx=30, pady=6, fill="x")

tk.Label(card, text="Password", bg="white", anchor="w").pack(fill="x", padx=30)
password_entry = tk.Entry(card, show="*", font=("Arial", 11))
password_entry.pack(padx=30, pady=6, fill="x")

# Confirm Password (only for register)
confirm_label = tk.Label(card, text="Confirm Password", bg="white", anchor="w")
confirm_entry = tk.Entry(card, show="*", font=("Arial", 11))

# ------------------ BUTTON ------------------

btn_canvas = tk.Canvas(card, width=260, height=42, highlightthickness=0)
btn_canvas.pack(pady=22)

def draw_button_gradient():
    for i in range(260):
        r = int(79 + (143 - 79) * (i / 260))
        g = int(172 + (0 - 172) * (i / 260))
        b = int(254 + (255 - 254) * (i / 260))
        color = f"#{r:02x}{g:02x}{b:02x}"
        btn_canvas.create_line(i, 0, i, 42, fill=color)

draw_button_gradient()

action_btn = tk.Button(
    card,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#8f00ff",
    activebackground="#6a00cc",
    relief="flat",
    bd=0,
    command=submit
)
btn_canvas.create_window(130, 21, window=action_btn)

# ------------------ SWITCH MODE ------------------

switch_btn = tk.Button(
    card,
    text="Not a member? Signup now",
    bg="white",
    fg="#4facfe",
    bd=0,
    cursor="hand2",
    command=switch_mode
)
switch_btn.pack()

root.mainloop()
