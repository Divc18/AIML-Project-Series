import tkinter as tk
from tkinter import scrolledtext
import re

memory = {}
question_list = ["What is your favorite color?", "What's your hobby?", "Which city are you from?"]
current_question = None

def chatbot_response(user_input):
    basic_questions = {
        "how are you": "I'm doing well, thank you! How are you?",
        "what is your name": "I’m Chatbot, your virtual assistant!",
        "what can you do": "I can chat with you, remember things, and help with basic queries.",
        "where are you from": "I come from the AI world to assist you.",
        "what is your purpose": "My purpose is to help make your life easier!"
    }

    for question in basic_questions:
        if re.search(rf'\b{question}\b', user_input):
            return basic_questions[question]

    return "I'm not sure I understand that. Could you please rephrase?"

def recall_previous_interactions():
    if not memory:
        return "We haven't discussed anything memorable yet."
    
    response = "Here's what I remember:\n"
    for key, value in memory.items():
        response += f"- You mentioned your {key} is {value}.\n"
    
    return response

def greet_user():
    return "Hello! I'm your chatbot. How can I assist you today?"

def farewell():
    return "Goodbye! It was nice chatting. Have a great day!"

def sentiment_response(user_input):
    positive_words = ['good', 'great', 'happy', 'awesome']
    negative_words = ['bad', 'sad', 'angry', 'upset']
    
    if any(word in user_input for word in positive_words):
        return "I'm glad you're feeling good!"
    elif any(word in user_input for word in negative_words):
        return "I'm sorry you're feeling that way."
    
    return ""

def handle_error():
    return "I didn't catch that. Please try again or type 'help' to see available commands."

def help_feature():
    return ("Here are some things you can ask me:\n"
            "- 'How are you?'\n"
            "- 'What’s your name?'\n"
            "- 'What can you do?'\n"
            "- 'Where are you from?'\n"
            "- 'What is your purpose?'\n"
            "- Type 'recall' to see what I remember.")

def ask_questions_and_store(user_input):
    global current_question

    if current_question:
        if "color" in current_question.lower():
            memory['favorite color'] = user_input
        elif "hobby" in current_question.lower():
            memory['hobby'] = user_input
        elif "city" in current_question.lower():
            memory['city'] = user_input
        
        current_question = next_question()

# Get the next question in the list
def next_question():
    global question_list
    if question_list:
        return question_list.pop(0)
    return None

def chatbot():
    global current_question

    user_input = entry.get().strip().lower()
    if not user_input:
        return  
    conversation_display.config(state=tk.NORMAL) 
    conversation_display.insert(tk.END, f"You: {user_input}\n")
    
    if user_input in ['bye', 'goodbye', 'exit', 'quit']:
        response = farewell()
        conversation_display.insert(tk.END, f"Chatbot: {response}\n")
        conversation_display.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        return
    
    if current_question:
        ask_questions_and_store(user_input)
        if current_question:
            conversation_display.insert(tk.END, f"Chatbot: {current_question}\n")
        else:
            conversation_display.insert(tk.END, f"Chatbot: Thank you for your answers!\n")
        conversation_display.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        return
    
    if user_input == 'help':
        response = help_feature()
    elif user_input == 'recall':
        response = recall_previous_interactions()
    elif user_input == 'ask me questions':
        current_question = next_question()
        if current_question:
            conversation_display.insert(tk.END, f"Chatbot: {current_question}\n")
    else:
        sentiment = sentiment_response(user_input)
        if sentiment:
            conversation_display.insert(tk.END, f"Chatbot: {sentiment}\n")
        
        response = chatbot_response(user_input)
        if response == "I'm not sure I understand that. Could you please rephrase?":
            response = handle_error()
    
    if response:
        conversation_display.insert(tk.END, f"Chatbot: {response}\n")
    conversation_display.config(state=tk.DISABLED)  
    entry.delete(0, tk.END)  

def display_memory():
    memory_window = tk.Toplevel(root)
    memory_window.title("Chatbot Memory")
    memory_window.geometry("300x300")
    memory_window.configure(bg="#E8F6F3")

    memory_label = tk.Label(memory_window, text="Chatbot Memory", font=("Helvetica", 14), bg="#85C1E9", fg="#1F618D")
    memory_label.pack(pady=10)

    memory_text = scrolledtext.ScrolledText(memory_window, wrap=tk.WORD, width=35, height=10, bg='#FBFCFC', fg='#154360', font=("Arial", 12))
    memory_text.pack(pady=10)

    memory_content = recall_previous_interactions()
    memory_text.insert(tk.END, memory_content)
    memory_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Chatbot Assistant")

root.geometry("500x600")
root.configure(bg='#E8F6F3')

title_label = tk.Label(root, text="Chatbot Assistant", font=("Helvetica", 16, "bold"), bg="#85C1E9", fg="#1B4F72", pady=10)
title_label.pack()

conversation_frame = tk.Frame(root, bg="#E8F6F3")
conversation_frame.pack(pady=10)

conversation_display = scrolledtext.ScrolledText(conversation_frame, wrap=tk.WORD, height=20, width=50, bg='#FDFEFE', fg='#154360', font=("Arial", 12))
conversation_display.pack()
conversation_display.insert(tk.END, f"Chatbot: {greet_user()}\n")
conversation_display.config(state=tk.DISABLED)

entry = tk.Entry(root, width=40, font=("Arial", 12), bd=2, relief=tk.SOLID)
entry.pack(pady=10)

button_frame = tk.Frame(root, bg='#E8F6F3')
button_frame.pack(pady=10)

send_button = tk.Button(button_frame, text="Send", width=12, command=chatbot, bg='#2980B9', fg='#FFFFFF', font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3)
send_button.grid(row=0, column=0, padx=5)

memory_button = tk.Button(button_frame, text="Memory", width=12, command=display_memory, bg='#1ABC9C', fg='#FFFFFF', font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3)
memory_button.grid(row=0, column=1, padx=5)

send_button.config(activebackground="#5499C7", activeforeground="#FFFFFF")
memory_button.config(activebackground="#48C9B0", activeforeground="#FFFFFF")

root.mainloop()
