import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import time
import os
from chatbot import get_response  
# from chatbot_ltsm import get_response  

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    entry.delete(0, tk.END)

    display_message(user_input, user_icon, "You", "#00ADB5")

    def bot_response():
        time.sleep(0.5)
        response = get_response(user_input)
        if isinstance(response, dict) and "text" in response:
            display_message(response["text"], bot_icon, "Bot", "#FF914D")
            if "image" in response and os.path.exists(response["image"]):
                display_image(response["image"])
        else:
            display_message(response, bot_icon, "Bot", "#FF914D")

    threading.Thread(target=bot_response, daemon=True).start()

def display_message(message, icon, sender, color):
    chat_area.config(state=tk.NORMAL)
    
    frame = tk.Frame(chat_area, bg="white")
    frame.pack(anchor="w" if sender == "Bot" else "e", fill="x", padx=5, pady=2)
    
    if sender == "Bot":
        label_icon = tk.Label(frame, image=icon, bg="white")
        label_icon.pack(side=tk.LEFT, padx=5)
    
    label_text = tk.Label(frame, text=message, wraplength=400, justify="left",
                          font=("Georgia", 13), fg=color, bg="white")
    label_text.pack(side=tk.LEFT if sender == "Bot" else tk.RIGHT, padx=5)
    
    if sender != "Bot":
        label_icon = tk.Label(frame, image=icon, bg="white")
        label_icon.pack(side=tk.RIGHT, padx=5)
    
    chat_area.window_create(tk.END, window=frame)
    chat_area.insert(tk.END, "\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def display_image(image_path):
    img = Image.open(image_path)
    img = img.resize((450, int((450/img.size[0])*img.size[0])))
    img = ImageTk.PhotoImage(img)

    def update_ui():
        chat_area.config(state=tk.NORMAL)

        frame = tk.Frame(chat_area, bg="white", width=chat_area.winfo_width())
        frame.pack(anchor='center', fill="x", padx=10, pady=10)

        img_container = tk.Frame(frame, bg="white")
        img_container.pack(expand=True, fill="both")

        img_container.grid_rowconfigure(0, weight=1)
        img_container.grid_columnconfigure(0, weight=1)

        img_label = tk.Label(img_container, image=img, bg="white")
        img_label.image = img
        img_label.grid(row=0, column=0)

        chat_area.window_create(tk.END, window=frame)
        chat_area.insert(tk.END, "\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)

    chat_area.after(0, update_ui)


# Giao diện Tkinter
root = tk.Tk()
root.title("Cuisine Chatbot")
root.geometry("500x650")
root.configure(bg="white")

# Load ảnh avatar
user_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\angry.jpg").resize((30, 30))
user_icon = ImageTk.PhotoImage(user_icon)

bot_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\chef_icon.png").resize((30, 30))
bot_icon = ImageTk.PhotoImage(bot_icon)

# Khu vực hiển thị tin nhắn
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", padx=10, pady=10)
chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
chat_area.config(font=("Georgia", 14))

# Khung nhập tin nhắn
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=5, padx=10, fill=tk.X)

entry = tk.Entry(input_frame, font=("Georgia", 13), bg="#EEEEEE", fg="black", insertbackground="black")
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Georgia", 12), bg="#00ADB5", fg="white")
send_button.pack(side=tk.RIGHT)

root.mainloop()
