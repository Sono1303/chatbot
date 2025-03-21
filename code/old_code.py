# import tkinter as tk
# from tkinter import scrolledtext
# import threading
# import time
# from chatbot import get_response 

# def send_message():
#     user_input = entry.get().strip().lower()
#     if not user_input:
#         return
#     chat_area.config(state=tk.NORMAL)
#     chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
#     chat_area.config(state=tk.DISABLED)
#     entry.delete(0, tk.END)
    
#     def stream_response():
#         response = get_response(user_input)
#         chat_area.config(state=tk.NORMAL)
#         chat_area.insert(tk.END, "Bot: ", "bot")
#         for char in response:
#             chat_area.insert(tk.END, char, "bot")
#             chat_area.update()
#             time.sleep(0.03)
#         chat_area.insert(tk.END, "\n")
#         chat_area.config(state=tk.DISABLED)
#         chat_area.yview(tk.END)
    
#     threading.Thread(target=stream_response, daemon=True).start()

# root = tk.Tk()
# root.title("Chatbot")
# root.state("zoomed")  
# root.minsize(500, 600)
# root.maxsize(500, 600)
# root.configure(bg="#222831")  

# chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, bg="#393E46", fg="white", insertbackground="white", padx=10, pady=10, borderwidth=0, relief="flat")
# chat_area.tag_config("user", foreground="#00ADB5", font=("Arial", 12, "bold"))
# chat_area.tag_config("bot", foreground="#FFD369", font=("Arial", 12, "italic"))
# chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# input_frame = tk.Frame(root, bg="#222831")
# input_frame.pack(pady=5, padx=10, fill=tk.X)

# entry = tk.Entry(input_frame, font=("Arial", 12), bg="#EEEEEE", fg="black", insertbackground="black", borderwidth=0, relief="flat")
# entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
# entry.bind("<Return>", lambda event: send_message())

# send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Arial", 12), bg="#00ADB5", fg="white", activebackground="#008C9E", activeforeground="white", borderwidth=0, relief="flat", padx=10, pady=5)
# send_button.pack(side=tk.RIGHT)

# root.mainloop()

# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# import threading
# import time
# # from chatbot_asia import get_response as get_asia_response
# # from chatbot_europe import get_response as get_europe_response
# # from chatbot_america import get_response as get_america_response
# from chatbot import get_response 

# # Biến lưu trữ model hiện tại (Mặc định: Châu Á)
# current_model = "Asia"

# # Hàm thay đổi mô hình chatbot
# def change_model(model):
#     global current_model
#     current_model = model
#     chat_area.config(state=tk.NORMAL)
#     chat_area.insert(tk.END, f"--- Switched to {model} Cuisine Chatbot ---\n", "system")
#     chat_area.config(state=tk.DISABLED)

# # Hàm gửi tin nhắn
# def send_message():
#     user_input = entry.get().strip()
#     if not user_input:
#         return

#     entry.delete(0, tk.END)

#     # Hiển thị tin nhắn User
#     display_message(user_input, user_icon, "You", "#00ADB5")

#     # Xử lý trả lời của bot trong luồng khác
#     def bot_response():
#         time.sleep(0.5)
#         if current_model == "Asia":
#             # response = get_asia_response(user_input)
#             response = get_response(user_input)
#         elif current_model == "Europe":
#             # response = get_europe_response(user_input)
#             response = get_response(user_input)
#         else:
#             # response = get_america_response(user_input)
#             response = get_response(user_input)

#         display_message(response, bot_icon, "Bot", "#FF914D")

#     threading.Thread(target=bot_response, daemon=True).start()

# # Hàm hiển thị tin nhắn với icon
# def display_message(message, icon, sender, color):
#     chat_area.config(state=tk.NORMAL)

#     # Tạo frame chứa icon và tin nhắn
#     frame = tk.Frame(chat_area, bg="white")
#     frame.pack(anchor="w", fill="x", padx=5, pady=2)

#     # Hiển thị icon
#     label_icon = tk.Label(frame, image=icon, bg="white")
#     label_icon.pack(side=tk.LEFT, padx=5)

#     # Hiển thị tin nhắn
#     label_text = tk.Label(frame, text=f"{sender}: {message}", wraplength=400, justify="left", font=("Arial", 12), fg=color, bg="white")
#     label_text.pack(side=tk.LEFT, padx=5)

#     chat_area.window_create(tk.END, window=frame)
#     chat_area.insert(tk.END, "\n")
#     chat_area.config(state=tk.DISABLED)
#     chat_area.yview(tk.END)

# # Khởi tạo giao diện Tkinter
# root = tk.Tk()
# root.title("Cuisine Chatbot")
# root.geometry("500x650")
# root.configure(bg="white")

# # Load ảnh avatar
# user_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\user_icon.png").resize((30, 30))
# user_icon = ImageTk.PhotoImage(user_icon)

# bot_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\chef_icon.png").resize((30, 30))
# bot_icon = ImageTk.PhotoImage(bot_icon)

# # Khu vực hiển thị tin nhắn
# chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, bg="white", fg="black", padx=10, pady=10)
# chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
# chat_area.tag_config("system", foreground="red", font=("Arial", 12, "bold"))

# # Khu vực chọn nền ẩm thực
# button_frame = tk.Frame(root, bg="white")
# button_frame.pack(pady=5, padx=10, fill=tk.X)

# btn_asia = tk.Button(button_frame, text="Asia", command=lambda: change_model("Asia"), font=("Arial", 12), bg="#FF5733", fg="white")
# btn_asia.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# btn_europe = tk.Button(button_frame, text="Europe", command=lambda: change_model("Europe"), font=("Arial", 12), bg="#33A1FF", fg="white")
# btn_europe.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# btn_america = tk.Button(button_frame, text="America", command=lambda: change_model("America"), font=("Arial", 12), bg="#33FF57", fg="white")
# btn_america.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# # Khung nhập tin nhắn
# input_frame = tk.Frame(root, bg="white")
# input_frame.pack(pady=5, padx=10, fill=tk.X)

# entry = tk.Entry(input_frame, font=("Arial", 12), bg="#EEEEEE", fg="black", insertbackground="black")
# entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
# entry.bind("<Return>", lambda event: send_message())

# send_button = tk.Button(input_frame, text="Send", command=lambda: send_message(), font=("Arial", 12), bg="#00ADB5", fg="white")
# send_button.pack(side=tk.RIGHT)

# root.mainloop()

# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# import threading
# import time
# from chatbot import get_response 

# # Biến lưu model hiện tại
# current_model = "Asia"

# # Hàm thay đổi mô hình chatbot
# def change_model(model):
#     global current_model
#     current_model = model
#     update_button_colors()
#     chat_area.config(state=tk.NORMAL)
#     # chat_area.insert(tk.END, f"\n--- Switched to {model} Cuisine Chatbot ---\n", "system")
#     chat_area.config(state=tk.DISABLED)

# # Cập nhật màu sắc nút khi chọn
# def update_button_colors():
#     for btn, model in cuisine_buttons.items():
#         if model == current_model:
#             btn.config(bg="darkblue", fg="white")  # Sáng màu khi chọn
#         else:
#             btn.config(bg="lightgray", fg="black")  # Màu nhạt khi không chọn

# # Gửi tin nhắn
# def send_message():
#     user_input = entry.get().strip()
#     if not user_input:
#         return
#     entry.delete(0, tk.END)

#     # Hiển thị tin nhắn User
#     display_message(user_input, user_icon, "You", "#00ADB5")

#     # Xử lý tin nhắn của bot
#     def bot_response():
#         time.sleep(0.5)
#         response = get_response(user_input)
#         display_message(response, bot_icon, "Bot", "#FF914D")

#     threading.Thread(target=bot_response, daemon=True).start()

# # Hiển thị tin nhắn với icon
# def display_message(message, icon, sender, color):
#     chat_area.config(state=tk.NORMAL)

#     frame = tk.Frame(chat_area, bg="white")
#     frame.pack(anchor="w" if sender == "Bot" else "e", fill="x", padx=5, pady=2)

#     label_icon = tk.Label(frame, image=icon, bg="white")
#     label_icon.pack(side=tk.LEFT if sender == "Bot" else tk.RIGHT, padx=5)

#     label_text = tk.Label(frame, text=message, wraplength=400, justify="left",
#                           font=("Arial", 12), fg=color, bg="white")
#     label_text.pack(side=tk.LEFT if sender == "Bot" else tk.RIGHT, padx=5)

#     chat_area.window_create(tk.END, window=frame)
#     chat_area.insert(tk.END, "\n")
#     chat_area.config(state=tk.DISABLED)
#     chat_area.yview(tk.END)

# # Giao diện Tkinter
# root = tk.Tk()
# root.title("Cuisine Chatbot")
# root.geometry("500x650")
# root.configure(bg="white")

# # Load ảnh avatar
# user_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\user_icon.png").resize((30, 30))
# user_icon = ImageTk.PhotoImage(user_icon)

# bot_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\chef_icon.png").resize((30, 30))
# bot_icon = ImageTk.PhotoImage(bot_icon)

# # Khu vực hiển thị tin nhắn
# chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, bg="white", fg="black", padx=10, pady=10)
# chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
# chat_area.tag_config("system", foreground="red", font=("Arial", 12, "bold"))

# # Khu vực chọn nền ẩm thực
# button_frame = tk.Frame(root, bg="white")
# button_frame.pack(pady=5, padx=10, fill=tk.X)

# cuisine_buttons = {}

# for model, color in [("Asia", "#FF5733"), ("Europe", "#33A1FF"), ("America", "#33FF57")]:
#     btn = tk.Button(button_frame, text=model, command=lambda m=model: change_model(m), font=("Arial", 12), bg="lightgray", fg="black")
#     btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
#     cuisine_buttons[btn] = model

# # Cập nhật màu nút ban đầu
# update_button_colors()

# # Khung nhập tin nhắn
# input_frame = tk.Frame(root, bg="white")
# input_frame.pack(pady=5, padx=10, fill=tk.X)

# entry = tk.Entry(input_frame, font=("Arial", 12), bg="#EEEEEE", fg="black", insertbackground="black")
# entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
# entry.bind("<Return>", lambda event: send_message())

# send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Arial", 12), bg="#00ADB5", fg="white")
# send_button.pack(side=tk.RIGHT)

# root.mainloop()

# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# import threading
# import time
# import os
# from chatbot import get_response  # Hàm xử lý phản hồi từ chatbot

# # Gửi tin nhắn
# def send_message():
#     user_input = entry.get().strip()
#     if not user_input:
#         return
#     entry.delete(0, tk.END)

#     # Hiển thị tin nhắn User
#     display_message(user_input, user_icon, "You", "#00ADB5")

#     # Xử lý tin nhắn của bot
#     def bot_response():
#         time.sleep(0.5)
#         response = get_response(user_input)
#         if isinstance(response, dict) and "text" in response:
#             display_message(response["text"], bot_icon, "Bot", "#FF914D")
#             if "image" in response and os.path.exists(response["image"]):
#                 display_image(response["image"])
#         else:
#             display_message(response, bot_icon, "Bot", "#FF914D")

#     threading.Thread(target=bot_response, daemon=True).start()

# # Hiển thị tin nhắn với icon
# def display_message(message, icon, sender, color):
#     chat_area.config(state=tk.NORMAL)
    
#     frame = tk.Frame(chat_area, bg="white")
#     frame.pack(anchor="e" if sender == "Bot" else "w", fill="x", padx=5, pady=2)
    
#     label_icon = tk.Label(frame, image=icon, bg="white")
#     label_icon.pack(side=tk.LEFT if sender == "Bot" else tk.RIGHT, padx=5)
    
#     label_text = tk.Label(frame, text=message, wraplength=400, justify="left",
#                           font=("Arial", 12), fg=color, bg="white")
#     label_text.pack(side=tk.LEFT if sender == "Bot" else tk.RIGHT, padx=5)
    
#     chat_area.window_create(tk.END, window=frame)
#     chat_area.insert(tk.END, "\n")
#     chat_area.config(state=tk.DISABLED)
#     chat_area.yview(tk.END)

# # Hiển thị hình ảnh món ăn
# def display_image(image_path):
#     img = Image.open(image_path).resize((150, 150))
#     img = ImageTk.PhotoImage(img)
    
#     chat_area.config(state=tk.NORMAL)
    
#     img_label = tk.Label(chat_area, image=img, bg="white")
#     img_label.image = img  # Lưu tham chiếu để không bị giải phóng bộ nhớ
#     chat_area.window_create(tk.END, window=img_label)
#     chat_area.insert(tk.END, "\n")
    
#     chat_area.config(state=tk.DISABLED)
#     chat_area.yview(tk.END)

# # Giao diện Tkinter
# root = tk.Tk()
# root.title("Cuisine Chatbot")
# root.geometry("500x650")
# root.configure(bg="white")

# # Load ảnh avatar
# user_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\user_icon.png").resize((30, 30))
# user_icon = ImageTk.PhotoImage(user_icon)

# bot_icon = Image.open(r"E:\Chatbot\Neural_network_chatbot\assets\chef_icon.png").resize((30, 30))
# bot_icon = ImageTk.PhotoImage(bot_icon)

# # Khu vực hiển thị tin nhắn
# chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, bg="white", fg="black", padx=10, pady=10)
# chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# # Khung nhập tin nhắn
# input_frame = tk.Frame(root, bg="white")
# input_frame.pack(pady=5, padx=10, fill=tk.X)

# entry = tk.Entry(input_frame, font=("Arial", 12), bg="#EEEEEE", fg="black", insertbackground="black")
# entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
# entry.bind("<Return>", lambda event: send_message())

# send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Arial", 12), bg="#00ADB5", fg="white")
# send_button.pack(side=tk.RIGHT)

# root.mainloop()

# import random
# import json
# import pickle
# import numpy as np
# import tensorflow as tf
# import tensorflow_hub as hub
# import tensorflow_text as text
# import nltk
# from sklearn.preprocessing import LabelEncoder

# # from tensorflow.keras import mixed_precision
# # mixed_precision.set_global_policy('mixed_float16')

# with open('intents.json', encoding='utf-8') as file:
#     intents = json.load(file)

# sentences = []
# labels = []

# for intent in intents['intents']:
#     for pattern in intent['patterns']:
#         sentences.append(pattern)
#         labels.append(intent['tag'])

# label_encoder = LabelEncoder()
# encoded_labels = label_encoder.fit_transform(labels)
# num_classes = len(set(encoded_labels))

# train_Y = tf.keras.utils.to_categorical(encoded_labels, num_classes=num_classes)

# bert_layer = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder/4", trainable=False)

# # train_X = np.array(bert_layer(sentences))
# train_Y = tf.keras.utils.to_categorical(encoded_labels, num_classes=num_classes)

# # train_dataset = tf.data.Dataset.from_tensor_slices((train_X, train_Y))
# # train_dataset = train_dataset.shuffle(buffer_size=1024).batch(64).prefetch(tf.data.AUTOTUNE)

# model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(), dtype=tf.string),  # BERT yêu cầu đầu vào là chuỗi
#     bert_layer,
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(num_classes, activation='softmax')
# ])

# # model = tf.keras.Sequential([
# #     tf.keras.layers.Input(shape=(train_X.shape[1],)),
# #     bert_layer,
# #     tf.keras.layers.Dense(128, activation='relu'),
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(num_classes, activation='softmax')
# # ])

# # model = tf.keras.Sequential([
# #     tf.keras.layers.Input(shape=(train_X.shape[1],)),
# #     tf.keras.layers.Reshape((1, train_X.shape[1])),
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(32, activation='relu'),
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(num_classes, activation='softmax')
# # ])

# # model = tf.keras.Sequential([
# #     tf.keras.layers.Input(shape=(train_X.shape[1],)),
# #     tf.keras.layers.Reshape((1, train_X.shape[1])),
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),  # Giảm từ 128 -> 64
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),  # Giảm từ 64 -> 32
# #     tf.keras.layers.GlobalMaxPooling1D(),  # Giảm số lượng tham số đầu ra
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(16, activation='relu'),  # Giảm từ 32 -> 16
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(num_classes, activation='softmax')
# # ])

# # optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
# # model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# # lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-5)

# # from tensorflow.keras.regularizers import l2

# # model = tf.keras.Sequential([
# #     tf.keras.layers.Input(shape=(train_X.shape[1],)),
# #     tf.keras.layers.Reshape((1, train_X.shape[1])),
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True, kernel_regularizer=l2(0.001))),
# #     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, kernel_regularizer=l2(0.001))),
# #     tf.keras.layers.GlobalMaxPooling1D(),
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(16, activation='relu', kernel_regularizer=l2(0.001)),
# #     tf.keras.layers.Dropout(0.5),
# #     tf.keras.layers.Dense(num_classes, activation='softmax')
# # ])

# optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
# model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# train_X = np.array(sentences) 
# history = model.fit(train_X, train_Y, epochs=200, batch_size=64, verbose=1)

# model.save('model/chatbot_bert_bilstm.keras')
# pickle.dump(label_encoder, open('model/label_encoder.pkl', 'wb'))

# print("Training complete! Chatbot model saved successfully.")