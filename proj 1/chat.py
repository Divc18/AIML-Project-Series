import tkinter as tk
from tkinter import scrolledtext

faq_data = {
    "admission procedure": "The admission procedure involves filling out an online application form, submitting required documents, and attending an interview.",
    "requirements": "The admission requirements include a high school diploma, transcripts, recommendation letters, and a completed application form.",
    "deadlines": "The application deadlines are as follows:\n- Early Admission: November 1\n- Regular Admission: January 15.",
    "scholarships": "We offer merit-based scholarships. Please check the official website for details.",
    "application fee": "The application fee is $50, which can be paid online during the application process."
}

# Function to handle user queries
def get_response(query):
    query = query.lower()
    response = faq_data.get(query, "I'm sorry, I don't have the answer to that question. Please check the official website or contact our admission office.")
    return response

# Function to add a message to the conversation
def add_message(user_message, bot_response):
    conversation_area.insert(tk.END, "You: " + user_message + "\n")
    conversation_area.insert(tk.END, "Bot: " + bot_response + "\n")
    conversation_area.yview(tk.END)

# Function to handle user input
def handle_user_input():
    user_message = user_input.get()
    if user_message.strip():
        bot_response = get_response(user_message)
        add_message(user_message, bot_response)
        user_input.delete(0, tk.END)

# Function to clear the conversation
def clear_conversation():
    conversation_area.delete(1.0, tk.END)

# Create the main application window
app = tk.Tk()
app.title("College Admission Q&A Bot")
app.geometry("500x600")
app.resizable(False, False)

app.configure(bg="#f0f8ff")

title_label = tk.Label(app, text="College Admission Q&A Bot", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#333333")
title_label.pack(pady=10)

conversation_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Arial", 12), width=50, height=20, bg="#ffffff", fg="#333333")
conversation_area.pack(pady=10)

user_input = tk.Entry(app, font=("Arial", 14), width=40, bg="#f5f5f5", fg="#333333")
user_input.pack(pady=5)

send_button = tk.Button(app, text="Send", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff", command=handle_user_input)
send_button.pack(pady=5)

clear_button = tk.Button(app, text="Clear", font=("Arial", 12), bg="#f44336", fg="#ffffff", command=clear_conversation)
clear_button.pack(pady=5)

app.mainloop()
