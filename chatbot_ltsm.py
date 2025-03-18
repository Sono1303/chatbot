# # import tensorflow_hub as hub
# # import tensorflow as tf

# # # Load mô hình với custom_objects
# # model = tf.keras.models.load_model(
# #     'model/chatbot_bert_bilstm.keras',
# #     custom_objects={'KerasLayer': hub.KerasLayer}  # ✅ Định nghĩa KerasLayer khi load mô hình
# # )

# # # Xem kiến trúc mô hình
# # model.summary()

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pickle
import json

def load_model():
    model = tf.keras.models.load_model('model/chatbot_bert.keras')
    return model

def predict_response(text_input, model, bert_layer, tag_to_response):
    # Chuyển văn bản thành vector embedding
    embedding = np.array(bert_layer([text_input]))

    # Dự đoán nhãn
    prediction = model.predict(embedding)
    predicted_label_idx = np.argmax(prediction)  # Lấy chỉ mục có xác suất cao nhất

    # Tải label encoder để chuyển index thành tag
    with open("model/label_encoder.pkl", "rb") as file:
        label_encoder = pickle.load(file)

    predicted_tag = label_encoder.inverse_transform([predicted_label_idx])[0]  # Chuyển index -> tag

    # Lấy phản hồi tương ứng với tag
    response = np.random.choice(tag_to_response.get(predicted_tag, ["I don't understand."]))
    return response

# Load mô hình và BERT
bert_layer = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
model = load_model()

# Tải dữ liệu intents
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

tag_to_response = {intent["tag"]: intent["responses"] for intent in intents["intents"]}

# Chạy thử dự đoán
# text = "Hi"
# response = predict_response(text, model, bert_layer, tag_to_response)
# print("Chatbot:", response)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye! 👋")
        break
    response = predict_response(user_input, model, bert_layer, tag_to_response)
    print("Chatbot:", response)
