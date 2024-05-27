# main.py
import tkinter as tk
from tkinter import scrolledtext
import requests
from config import OPENAI_API_KEY

class ChatGPTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT GUI")
        self.create_widgets()

    def create_widgets(self):
        self.custom_instruction_label = tk.Label(self.root, text="Custom Instruction:")
        self.custom_instruction_label.pack()

        self.custom_instruction_entry = tk.Entry(self.root, width=50)
        self.custom_instruction_entry.pack()

        self.chat_label = tk.Label(self.root, text="Chat:")
        self.chat_label.pack()

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.chat_area.pack()

        self.input_label = tk.Label(self.root, text="Your Message:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def send_message(self):
        user_message = self.input_entry.get()
        custom_instruction = self.custom_instruction_entry.get()

        self.chat_area.insert(tk.END, "You: " + user_message + "\n")

        response = self.get_response_from_chatgpt(user_message, custom_instruction)
        self.chat_area.insert(tk.END, "ChatGPT: " + response + "\n")

        self.input_entry.delete(0, tk.END)

    def get_response_from_chatgpt(self, message, instruction):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": message},
            ]
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return "Error: Unable to get response from ChatGPT"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGPTApp(root)
    root.mainloop()
