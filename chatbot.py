import random
import json
import pickle
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import threading
import nltk
from nltk.stem import WordNetLemmatizer
import time
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.load(open('intents.json'))
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))
model = load_model('model/chatbot_model.keras')

def clean_up_sentence(sentence):
    return [lemmatizer.lemmatize(word) for word in nltk.word_tokenize(sentence)]

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    return np.array([1 if word in sentence_words else 0 for word in words])

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = sorted([[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD], key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

def get_response(intents_list):
    if not intents_list:
        return "Sorry, can you ask me again?"
    tag = intents_list[0]['intent']
    for i in intents['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Sorry, can you ask me again?"

def send_message():
    user_input = entry.get().strip().lower()
    if not user_input:
        return
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    chat_area.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    
    def stream_response():
        response = get_response(predict_class(user_input))
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Bot: ", "bot")
        for char in response:
            chat_area.insert(tk.END, char, "bot")
            chat_area.update()
            time.sleep(0.03)
        chat_area.insert(tk.END, "\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    
    threading.Thread(target=stream_response, daemon=True).start()

root = tk.Tk()
root.title("Chatbot")
root.state("zoomed")  
root.minsize(500, 600)
root.maxsize(500, 600)
root.configure(bg="#222831")  

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, bg="#393E46", fg="white", insertbackground="white", padx=10, pady=10, borderwidth=0, relief="flat")
chat_area.tag_config("user", foreground="#00ADB5", font=("Arial", 12, "bold"))
chat_area.tag_config("bot", foreground="#FFD369", font=("Arial", 12, "italic"))
chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root, bg="#222831")
input_frame.pack(pady=5, padx=10, fill=tk.X)

entry = tk.Entry(input_frame, font=("Arial", 12), bg="#EEEEEE", fg="black", insertbackground="black", borderwidth=0, relief="flat")
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Arial", 12), bg="#00ADB5", fg="white", activebackground="#008C9E", activeforeground="white", borderwidth=0, relief="flat", padx=10, pady=5)
send_button.pack(side=tk.RIGHT)

root.mainloop()
