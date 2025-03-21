from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, scrolledtext
from PIL import Image, ImageTk
import threading
import time
import os
from chatbot import get_response  # Adjust this import to your actual chatbot function

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Chatbot\Neural_network_chatbot\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    entry.delete(0, 'end')

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
    chat_area.config(state='normal')
    frame = Canvas(chat_area, bg=color, width=360, height=50)
    frame.create_text(10, 25, anchor='w', text=message, fill='white', font=("Georgia", 13), width=340)
    chat_area.window_create('end', window=frame)
    chat_area.insert('end', "\n")
    chat_area.config(state='disabled')
    chat_area.yview('end')

def display_image(image_path):
    img = Image.open(image_path).resize((200, 200))
    img = ImageTk.PhotoImage(img)
    label = Canvas(chat_area, bg="white", width=200, height=200)
    label.create_image(100, 100, image=img)
    label.image = img
    chat_area.window_create('end', window=label)
    chat_area.insert('end', "\n")
    chat_area.config(state='disabled')
    chat_area.yview('end')

# GUI Initialization
window = Tk()
window.geometry("422x750")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=750,
    width=422,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(0.0, 0.0, 422.0, 750.0, fill="#FFFFFF", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(211.0, 43.0, image=image_image_1)

canvas.create_text(120.0, 30.0, anchor="nw", text="Cuisine Chatbot", fill="#FFFFFF", font=("Nunito", 24))

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(211.0, 689.0, image=image_image_2)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=send_message,
    relief="flat"
)
button_1.place(x=336.0, y=665.0, width=44.0, height=47.0)

# Chat Area
chat_area = scrolledtext.ScrolledText(window, wrap='word', state='disabled', bg="#F0F0F0", fg="black", padx=10, pady=10)
chat_area.place(x=10, y=100, width=400, height=500)

# User Input
entry = Entry(window, font=("Georgia", 13), bg="#EEEEEE", fg="black")
entry.place(x=10, y=665, width=310, height=47)
entry.bind("<Return>", lambda event: send_message())

# Icons
user_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\angry.jpg").resize((30, 30))
user_icon = ImageTk.PhotoImage(user_icon)

bot_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\chef_icon.png").resize((30, 30))
bot_icon = ImageTk.PhotoImage(bot_icon)

window.resizable(False, False)
window.mainloop()
