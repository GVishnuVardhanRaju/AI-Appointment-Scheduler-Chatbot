The AI Appointment Scheduler Chatbot is a desktop-based application and rule based ai system developed using Python and the Tkinter GUI framework to simplify and automate the process of booking and managing appointments within an organization.

The system provides a secure login mechanism, an AI-powered chatbot for interaction, and automated email notifications, ensuring efficient communication and smooth appointment management.

MySQL is used for backend purpose for storing:

Users History
Chatbot History

🌟 Key Features

🔐 Secure Authentication System

User login with encrypted credentials

Password hashing for security

Protection against unauthorized access

🤖 AI Chatbot Assistant

Responds to user queries instantly

Guides users through appointment booking

Provides information about staff availability

📅 Appointment Management

Book appointments easily

Manage and view appointment records

Organized scheduling system

📧 Email Notifications

Appointment confirmation emails

Reminder notifications

Update alerts for users

🗄 Database Integration

Stores user profiles

Maintains chat history

Saves appointment records for future reference

🛠️ Technologies Used

Programming Language

Python

GUI Framework

Tkinter

Database

SQLite / MySQL

Libraries

smtplib (Email notifications)

hashlib / bcrypt (Password encryption)

datetime

Security Concepts

Password hashing

Secure authentication

Controlled database access

📂 Project Structure
AI-Appointment-Scheduler-Chatbot/
│
├── app.py
├── login.py
├── db.py

⚙️ Installation Guide

Follow these steps to run the project locally.

1️⃣ Clone the Repository
git clone https://github.com/yourusername/ai-appointment-scheduler-chatbot.git

2️⃣ Navigate to Project Folder
cd ai-appointment-scheduler-chatbot

3️⃣ Run the Application
python login.py

💻 How It Works

User opens the application.

Secure login authentication verifies credentials.

After login, the AI chatbot interface appears.

Users interact with the chatbot to:

Ask questions

Check staff availability

Book appointments

Appointment data is stored in the database.

Confirmation and reminder emails are automatically sent.

🔐 Security Features

Password hashing using secure algorithms

Encrypted authentication process

Secure database interaction

Protection against unauthorized login attempts

🚀 Future Improvements

Voice-based chatbot interaction

Online web-based version

Admin dashboard for appointment management

Integration with Google Calendar

SMS notification system

🎯 Project Purpose

This project was developed to:

Demonstrate AI chatbot integration in desktop applications

Implement secure authentication mechanisms

Automate appointment scheduling processes

Apply cybersecurity principles in application development

👨‍💻 Author

G Vishnu Vardhan Raju