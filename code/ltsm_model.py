

import json
import pickle
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import LabelEncoder

JSON_PATH = r"E:\Chatbot\Neural_network_chatbot\data\intents.json"
LABEL_PATH = r'E:\Chatbot\Neural_network_chatbot\model\label_encoder.pkl'
MODEL_PATH = r'E:\Chatbot\Neural_network_chatbot\model\chatbot_bert.keras'

# Load dữ liệu intents.json
with open(JSON_PATH, encoding='utf-8') as file:
    intents = json.load(file)

sentences = []
labels = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        sentences.append(pattern)
        labels.append(intent['tag'])

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(set(encoded_labels))
train_Y = tf.keras.utils.to_categorical(encoded_labels, num_classes=num_classes)

# Load BERT Universal Sentence Encoder (USE)
bert_layer = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Chuyển đổi câu thành vector embedding (512 chiều)
train_X = np.array(bert_layer(sentences))

# Tạo mô hình
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(512,)),  # Đầu vào từ USE là (512,)
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Compile model
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Train model
history = model.fit(train_X, train_Y, epochs=200, batch_size=64, verbose=1)

# Lưu model và label_encoder
model.save(MODEL_PATH)
pickle.dump(label_encoder, open(LABEL_PATH, 'wb'))

print("Training complete! Model saved successfully.")
