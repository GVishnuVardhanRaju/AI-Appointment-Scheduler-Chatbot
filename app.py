import tkinter as tk
from tkinter import ttk
from datetime import datetime
import smtplib
from email.message import EmailMessage
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
from db import get_connection

SAVE_SYSTEM_MESSAGES = False

# ================= USER SESSION ================= #
logged_in_user_id = None
logged_in_user = "Guest"

if len(sys.argv) >= 3:
    logged_in_user_id = int(sys.argv[1])
    logged_in_user = sys.argv[2]

# ================= SMTP CONFIG ================= #
SMTP_EMAIL = "thundervardhan@gmail.com"
SMTP_PASSWORD = "tqpj cymu vhpc dxgs"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ================= DATA ================= #
DATA = {
    "CEO": [
        {"name": "Ratan Sharma", "age": 58, "profession": "Chief Executive Officer", "available": True, "appointments": []},
        {"name": "Anil Verma", "age": 55, "profession": "Chief Executive Officer", "available": False, "appointments": []},
    ],
    "CTO": [
        {"name": "Rahul Nair", "age": 42, "profession": "Chief Technology Officer", "available": True, "appointments": []},
        {"name": "Arjun Rao", "age": 45, "profession": "Chief Technology Officer", "available": True, "appointments": []},
    ],
    "COO": [
        {"name": "Prakash Menon", "age": 48, "profession": "Chief Operations Officer", "available": False, "appointments": []},
        {"name": "Nitin Joshi", "age": 50, "profession": "Chief Operations Officer", "available": True, "appointments": []},
    ],
    "CMO": [
        {"name": "Neha Kapoor", "age": 38, "profession": "Chief Marketing Officer", "available": True, "appointments": []},
        {"name": "Pooja Singh", "age": 40, "profession": "Chief Marketing Officer", "available": False, "appointments": []},
    ],
    "Manager": [
        {"name": "Rohit Agarwal", "age": 35, "profession": "Operations Manager", "available": True, "appointments": []},
        {"name": "Sunil Chawla", "age": 37, "profession": "Operations Manager", "available": True, "appointments": []},
    ],
}

# ================= EMAIL ================= #
def send_confirmation_email(to_email, person, data):
    msg = EmailMessage()
    msg["Subject"] = "Appointment Confirmation"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg.set_content(
        f"""
Hello {data['user_name']},

Your appointment has been scheduled successfully.

With    : {person['name']} ({person['profession']})
Purpose : {data['purpose']}
Date    : {data['date']}
Time    : {data['time']}

Regards,
AI Appointment Scheduler
"""
    )
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        return False

# ================= DATABASE ================= #
def save_chat(sender, message):
    if not logged_in_user_id:
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, sender, message) VALUES (%s, %s, %s)",
        (logged_in_user_id, sender, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

def load_chat_history():
    if not logged_in_user_id:
        return False
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT sender, message FROM chat_history WHERE user_id=%s ORDER BY timestamp",
        (logged_in_user_id,)
    )
    rows = cursor.fetchall()
    chat.config(state="normal")
    for row in rows:
        tag = "user" if row["sender"] == "user" else "bot"
        chat.insert("end", f"{row['message']}\n\n", tag)
    chat.config(state="disabled")
    cursor.close()
    conn.close()
    return len(rows) > 0

# ================= UI ================= #
root = tk.Tk()
root.title("AI Appointment Scheduler")
root.geometry("1200x750")
root.configure(bg="#1e1e1e")

left = tk.Frame(root, bg="#1e1e1e")
left.pack(side="left", fill="both", expand=True)

right = tk.Frame(root, bg="#121212")

chat = tk.Text(left, bg="#1e1e1e", fg="white", font=("Segoe UI", 12), wrap="word")
chat.pack(expand=True, fill="both", padx=15, pady=15)
chat.config(state="disabled", padx=10, pady=10, spacing3=5, spacing1=5, relief="flat")

entry = tk.Entry(left, font=("Segoe UI", 12))
entry.pack(fill="x", padx=15, pady=5)

send_btn = tk.Button(left, text="Send", bg="#3a7ff6", fg="white", font=("Segoe UI", 12, "bold"))
send_btn.pack(pady=5)

# ================= CHAT TAGS ================= #
chat.tag_configure(
    "user",
    justify="right",
    foreground="white",
    background="#25D366",
    lmargin1=50, lmargin2=10, rmargin=10,
    spacing1=5, spacing3=5,
    font=("Segoe UI", 12, "bold")
)
chat.tag_configure(
    "bot",
    justify="left",
    foreground="white",
    background="#3a3a3a",
    lmargin1=10, lmargin2=10, rmargin=50,
    spacing1=5, spacing3=5,
    font=("Segoe UI", 12)
)

bot_message_queue = []
bot_animating = False

def animated_bot_enqueue(text, save=True):
    global bot_animating
    bot_message_queue.append((text, save))
    if not bot_animating:
        bot_animating = True
        animated_bot_dequeue()

def animated_bot_dequeue(i=0):
    global bot_animating
    if not bot_message_queue:
        bot_animating = False
        return
    text, save = bot_message_queue[0]
    chat.config(state="normal")
    if i == 0:
        chat.insert("end", "🤖 ", "bot")
    if i < len(text):
        chat.insert("end", text[i], "bot")
        chat.after(20, animated_bot_dequeue, i + 1)
    else:
        chat.insert("end", "\n\n")
        if save:
            save_chat("bot", text)
        bot_message_queue.pop(0)
        chat.after(300, animated_bot_dequeue)
    chat.config(state="disabled")
    chat.see("end")

def user(msg):
    chat.config(state="normal")
    chat.insert("end", f"{msg}\n\n", "user")
    chat.config(state="disabled")
    chat.see("end")
    save_chat("user", msg)

# ================= DASHBOARD ================= #
dashboard_title = tk.Label(right, text="📊 Appointers Dashboard", bg="#121212", fg="white", font=("Segoe UI", 18, "bold"))
dashboard_title.pack(pady=(15,5))

profile = tk.Frame(right, bg="#181818")
profile.pack(fill="x", padx=15, pady=15)

labels = {}
for f in ["Role", "Name", "Age", "Profession", "Availability", "Appointments"]:
    lbl = tk.Label(profile, fg="white", bg="#181818", font=("Segoe UI", 11))
    lbl.pack(anchor="w")
    labels[f] = lbl

fig, ax = plt.subplots(figsize=(5,3))
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

def show_dashboard(role, person=None):
    right.pack(side="right", fill="both")
    dashboard_title.config(text=f"📊 {role} Appointers Dashboard")
    if person:
        labels["Role"].config(text=f"Role: {role}")
        labels["Name"].config(text=f"Name: {person['name']}")
        labels["Age"].config(text=f"Age: {person['age']}")
        labels["Profession"].config(text=f"Profession: {person['profession']}")
        labels["Availability"].config(text=f"Availability: {'Available ✅' if person['available'] else 'Unavailable ❌'}")
        labels["Appointments"].config(text=f"Appointments: {len(person['appointments'])}")
    ax.clear()
    ax.bar([p["name"] for p in DATA[role]], [len(p["appointments"]) for p in DATA[role]], color="#3a7ff6")
    ax.set_title(f"{role} Analytics")
    ax.tick_params(axis="x", rotation=45)
    canvas.draw()

# ================= DATE & TIME PICKERS ================= #
def date_picker(callback):
    win = tk.Toplevel(root)
    win.title("Select Date")
    cal = Calendar(win, date_pattern="yyyy-mm-dd")
    cal.pack(padx=10, pady=10)
    ttk.Button(win, text="Select", command=lambda: (callback(cal.get_date()), win.destroy())).pack()

def time_picker(callback):
    win = tk.Toplevel(root)
    win.title("Select Time")
    hour = ttk.Combobox(win, values=[f"{i:02d}" for i in range(24)], width=5)
    minute = ttk.Combobox(win, values=["00","15","30","45"], width=5)
    hour.pack(pady=5)
    minute.pack(pady=5)
    ttk.Button(win, text="Select", command=lambda: (callback(f"{hour.get()}:{minute.get()}"), win.destroy())).pack(pady=5)

# ================= STATE ================= #
appointment_flow = None
appointment_data = {}
selected_role = None
selected_person = None
mode = None
step = "start"

# ================= CHAT LOGIC ================= #
def on_date_selected(date):
    appointment_data["date"] = date
    animated_bot_enqueue(f"📅 Date selected: {date}")
    animated_bot_enqueue("Select appointment time:")
    time_picker(on_time_selected)

def on_time_selected(time):
    appointment_data["time"] = time
    animated_bot_enqueue(f"⏰ Time selected: {time}")
    summary = (
        f"Please confirm your appointment details (yes/no):\n"
        f"Name: {appointment_data['user_name']}\n"
        f"Email: {appointment_data['email']}\n"
        f"Purpose: {appointment_data['purpose']}\n"
        f"Date: {appointment_data['date']}\n"
        f"Time: {appointment_data['time']}\n"
        f"With: {selected_person['name']} ({selected_person['profession']})"
    )
    animated_bot_enqueue(summary)
    global appointment_flow
    appointment_flow = "await_confirmation"

def send(event=None):
    global step, mode, selected_role, selected_person, appointment_flow, appointment_data
    msg = entry.get().strip()
    entry.delete(0, "end")
    if not msg:
        return
    user(msg)

    # ================= APPOINTMENT FLOW ================= #
    if appointment_flow:
        if appointment_flow == "name":
            appointment_data["user_name"] = msg
            animated_bot_enqueue("Enter your email:")
            appointment_flow = "email"
            return
        if appointment_flow == "email":
            appointment_data["email"] = msg
            animated_bot_enqueue("Purpose of appointment:")
            appointment_flow = "purpose"
            return
        if appointment_flow == "purpose":
            appointment_data["purpose"] = msg
            animated_bot_enqueue("Select appointment date:")
            appointment_flow = "date"
            date_picker(on_date_selected)
            return
        if appointment_flow == "await_confirmation":
            if msg.lower() in ["yes","y"]:
                selected_person["appointments"].append(appointment_data.copy())
                animated_bot_enqueue("✅ Appointment booked successfully!")
                show_dashboard(selected_role, selected_person)
                if send_confirmation_email(appointment_data["email"], selected_person, appointment_data):
                    animated_bot_enqueue(f"📧 Confirmation email sent to {appointment_data['email']}")
                else:
                    animated_bot_enqueue("⚠️ Email failed, but appointment saved.")
            else:
                animated_bot_enqueue("❌ Appointment cancelled.")
            appointment_flow = None
            appointment_data = {}
            step = "start"
            animated_bot_enqueue("How can I help you more?")
            return

    # ================= STEP LOGIC ================= #
    if step == "start":
        if msg.lower() in ["appointment","availability","predict"]:
            mode = msg.lower()
            animated_bot_enqueue("Select role: " + ", ".join(DATA.keys()))
            step = "role"
        else:
            animated_bot_enqueue("Type: appointment | availability | predict")
        return

    if step == "role":
        if msg in DATA:
            selected_role = msg
            if mode == "availability":
                animated_bot_enqueue("Available people:")
                for p in DATA[msg]:
                    animated_bot_enqueue(f"{p['name']} - {'Available' if p['available'] else 'Unavailable'}")
                show_dashboard(msg)
                animated_bot_enqueue("Would you like to book an appointment? (yes/no)")
                step = "schedule_prompt"
            elif mode == "predict":
                best = min(DATA[msg], key=lambda x: len(x["appointments"]))
                selected_person = best
                animated_bot_enqueue(f"Best person: {best['name']}")
                animated_bot_enqueue("Suggested time slots: 10–11 AM, 4–5 PM")
                show_dashboard(msg, best)
                animated_bot_enqueue("Would you like to book with this person? (yes/no)")
                step = "schedule_confirm"
            elif mode == "appointment":
                animated_bot_enqueue("Select person:")
                for p in DATA[msg]:
                    animated_bot_enqueue(p["name"])
                step = "person"
        else:
            animated_bot_enqueue("Invalid role.")
        return

    if step == "schedule_prompt":
        if msg.lower() in ["yes","y"]:
            animated_bot_enqueue("Select person:")
            for p in DATA[selected_role]:
                if p["available"]:
                    animated_bot_enqueue(p["name"])
            step = "person"
        else:
            animated_bot_enqueue("Okay. How can I help you?")
            step = "start"
        return

    if step == "schedule_confirm":
        if msg.lower() in ["yes","y"]:
            appointment_flow = "name"
            animated_bot_enqueue("Please enter your full name:")
            step = None
        else:
            animated_bot_enqueue("Okay. How can I help you?")
            step = "start"
        return

    if step == "person":
        for p in DATA[selected_role]:
            if msg == p["name"] and p["available"]:
                selected_person = p
                show_dashboard(selected_role, selected_person)
                appointment_flow = "name"
                animated_bot_enqueue("Please enter your full name:")
                return
        animated_bot_enqueue("Invalid or unavailable person.")

send_btn.config(command=send)
entry.bind("<Return>", send)

# ================= LOAD HISTORY ================= #
has_history = load_chat_history()
if not has_history:
    animated_bot_enqueue(f"Welcome back, {logged_in_user} 👋", save=False)
    animated_bot_enqueue(
        "👋 Welcome to the AI Appointment Scheduler!\n"
        "I can help you book meetings, check availability, or suggest the best person to meet.\n\n"
        "💡 Try typing one of these:\n"
        "• appointment – Book a new appointment\n"
        "• availability – Check who’s available\n"
        "• predict – Get the best recommendation",
        save=False
    )

root.mainloop()
