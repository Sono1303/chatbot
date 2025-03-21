# import dearpygui.dearpygui as dpg

# dpg.create_context()

# with dpg.window(label="Cửa sổ chính", width=400, height=300):
#     dpg.add_text("Hello, Dear PyGui!")
#     dpg.add_button(label="Nhấn vào đây", callback=lambda: print("Button Clicked!"))

# dpg.create_viewport(title='Demo Dear PyGui', width=600, height=400)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

import random
import json
import pickle
import numpy as np
import time
import threading
import nltk
from nltk.stem import WordNetLemmatizer
import dearpygui.dearpygui as dpg
from keras.models import load_model
from PIL import Image

# Load dữ liệu chatbot
lemmatizer = WordNetLemmatizer()
intents = json.load(open('intents.json'))
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))
model = load_model(r'E:\Chatbot\Neural_network_chatbot\model\chatbot_model.keras')

# Load ảnh avatar
USER_AVATAR = "assets/user_icon.png"
BOT_AVATAR = "assets/chef_icon.png"

def load_texture(file_path, tag):
    try:
        image = Image.open(file_path).convert("RGBA")
        width, height = image.size
        data = np.array(image).flatten() / 255.0  # Chuẩn hóa pixel (0-1)
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag=tag)
        return True
    except Exception as e:
        print(f"Không thể load ảnh {file_path}: {e}")
        return False

# Load ảnh avatar
if load_texture(USER_AVATAR, "user_avatar") and load_texture(BOT_AVATAR, "bot_avatar"):
    print("Ảnh avatar đã load thành công!")
else:
    print("Lỗi khi load avatar!")

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

def display_message(user, text, avatar):
    with dpg.group(horizontal=True, parent="chat_window"):
        if dpg.does_alias_exist(avatar):  # Kiểm tra ảnh có tồn tại không
            dpg.add_image(avatar, width=30, height=30)
        else:
            dpg.add_text("[Ảnh lỗi]", color=(255, 0, 0))  # Báo lỗi nếu không load được ảnh
        dpg.add_text(text, color=(0, 0, 0) if user == "You" else (0, 0, 200))  # Chữ bot xanh đậm


# Gửi tin nhắn từ người dùng
def send_message():
    user_input = dpg.get_value("input_text").strip().lower()
    if not user_input:
        return
    dpg.set_value("input_text", "")  # Xóa ô nhập

    # Hiển thị tin nhắn người dùng
    display_message("You", f"You: {user_input}", USER_AVATAR)

    # Xử lý phản hồi chatbot
    def stream_response():
        response = get_response(predict_class(user_input))
        with dpg.group(horizontal=True, parent="chat_window"):
            dpg.add_image(BOT_AVATAR, width=30, height=30)
            text_id = dpg.add_text("Bot: ", color=(0, 0, 255))  # Màu xanh để phân biệt bot
        
        # Hiệu ứng gõ từng chữ
        typed_text = ""
        for char in response:
            typed_text += char
            dpg.set_value(text_id, typed_text)
            time.sleep(0.03)
    
    threading.Thread(target=stream_response, daemon=True).start()

# Cấu hình Dear PyGui
dpg.create_context()
dpg.create_viewport(title="Chatbot - Dear PyGui", width=500, height=600)

# Load hình ảnh avatar
with dpg.texture_registry():
    dpg.add_dynamic_texture(30, 30, [255, 255, 255, 255], tag=USER_AVATAR)
    dpg.add_dynamic_texture(30, 30, [255, 255, 255, 255], tag=BOT_AVATAR)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255))  # Nền trắng
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255))  # Nền trắng cho vùng chat
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))  # Chữ đen
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200))  # Nút xám nhạt
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (170, 170, 170))  # Hiệu ứng hover
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (150, 150, 150))  # Hiệu ứng nhấn nút

# Thiết kế giao diện
with dpg.window(label="Chatbot", width=500, height=600):
    with dpg.child_window(tag="chat_window", width=-1, height=500):
        dpg.add_text("Welcome to Chatbot!", color=(0, 0, 255))  # Bot có màu xanh

    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="input_text", hint="Type your message...", width=-100)
        dpg.add_button(label="Send", callback=send_message)

dpg.bind_theme(global_theme)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

