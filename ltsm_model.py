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

import json
import pickle
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import LabelEncoder

# Load dữ liệu intents.json
with open('intents.json', encoding='utf-8') as file:
    intents = json.load(file)

sentences = []
labels = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        sentences.append(pattern)
        labels.append(intent['tag'])

# Encode nhãn
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
model.save('model/chatbot_bert.keras')
pickle.dump(label_encoder, open('model/label_encoder.pkl', 'wb'))

print("Training complete! Model saved successfully.")
