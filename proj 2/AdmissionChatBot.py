import customtkinter as ctk  
import spacy
import json
import os

nlp = spacy.load('en_core_web_sm')

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

class AdmissionChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("College Admission Q&A Bot")
        self.root.geometry("690x520")

        self.chat_area = ctk.CTkTextbox(self.root, wrap="word", width=550, height=400, corner_radius=10, state='disabled')
        self.chat_area.grid(row=0, column=0, padx=10, pady=10)

        self.user_entry = ctk.CTkEntry(self.root, width=450, height=30, corner_radius=10)
        self.user_entry.grid(row=1, column=0, padx=10, pady=10)
        self.user_entry.bind("<Return>", self.process_query)  

        self.send_button = ctk.CTkButton(self.root, text="Send", width=100, height=30, corner_radius=10, command=self.process_query)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.context_memory = {}

        self.admission_info = self.load_admission_info()
        self.pending_keywords = None  

    def load_admission_info(self):
        
        if os.path.exists('admission_info.json'):
            with open('admission_info.json', 'r') as file:
                return json.load(file)
        else:
            return {}

    def process_query(self, event=None):
        user_query = self.user_entry.get().lower()
        self.user_entry.delete(0, ctk.END)
        
        self.update_chat(f"You: {user_query}")
        
        if self.pending_keywords:
            self.save_user_answer(user_query)
        else:
            response = self.get_response(user_query)
            self.update_chat(f"Bot: {response}")
    
    def get_response(self, query):
        doc = nlp(query)
        
        keywords = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB']]  
        
        for keyword in keywords:
            if keyword in self.admission_info:
                self.context_memory[keyword] = True
                return self.admission_info[keyword]
        
        return self.train_bot(query, keywords)

    def train_bot(self, query, keywords):
        
        self.update_chat("Bot: I don't know the answer to that. Can you please provide the answer?")
        self.pending_keywords = keywords  
        return "Please type the correct answer below and press Enter."

    def save_user_answer(self, user_answer):
        
        if user_answer and self.pending_keywords:
            key = self.pending_keywords[0]  # Choose the first keyword as the key for simplicity
            self.admission_info[key] = user_answer
            self.save_admission_info()

            # Reset pending keywords after saving
            self.pending_keywords = None

            # Notify the user that the information was saved
            self.update_chat(f"Bot: Thanks! I have stored the information about '{key}'.")

    def save_admission_info(self):
        
        with open('admission_info.json', 'w') as file:
            json.dump(self.admission_info, file, indent=4)

    def update_chat(self, message):
        
        self.chat_area.configure(state='normal')
        self.chat_area.insert(ctk.END, message + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(ctk.END)

# Main application loop
if __name__ == "__main__":
    root = ctk.CTk()  
    chatbot = AdmissionChatBot(root)
    root.mainloop()
