# import tensorflow as tf

# print("GPU Available:", tf.config.list_physical_devices('GPU'))

# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)  # Tránh bị hết VRAM
#         print("GPU is enabled!")
#     except RuntimeError as e:
#         print(e)

# import os

# model_path = r"E:\Chatbot\Neural_network_chatbot\model\chatbot_model.keras"
# if os.path.exists(model_path):
#     print("✅ File tồn tại")
# else:
#     print("❌ File không tồn tại")

# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  

# import tensorflow as tf

import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from init import extract_ingredients

# nltk.download('punkt')
# nltk.download('wordnet')

JSON_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'

lemmatizer = WordNetLemmatizer()

with open(JSON_PATH) as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_chars = {'?', '!', '.', ','}

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = extract_ingredients(pattern)
        print(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

print(len(words))
words = set(words)
print(len(words))
print(words)

