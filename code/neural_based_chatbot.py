import random
import json
import pickle
import numpy as np
import tensorflow as tf
from init import extract_ingredients, lemmatizer

JSON_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'
WORDS_PATH = r'E:\Chatbot\Neural_network_chatbot\model\words.pkl'
CLASSES_PATH = r'E:\Chatbot\Neural_network_chatbot\model\classes.pkl'
MODEL_PATH = r'E:\Chatbot\Neural_network_chatbot\model\chatbot_bert.keras'
HISTORY_PATH = r'E:\Chatbot\Neural_network_chatbot\model\history.pkl'

def train_chatbot(data):
    intents = json.load(open(data))

    words = []
    classes = []
    documents = []
    ignore_chars = {'?', '!', '.', ','}

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = extract_ingredients(pattern)
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # words = sorted(set(lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars)
    words = sorted(set(words))
    classes = sorted(set(classes))

    pickle.dump(words, open(WORDS_PATH, 'wb'))
    pickle.dump(classes, open(CLASSES_PATH, 'wb'))

    training = []
    output_empty = [0] * len(classes)

    for word_list, tag in documents:
        bag = [1 if word in [lemmatizer.lemmatize(w.lower()) for w in word_list] else 0 for word in words]
        output_row = output_empty[:]
        output_row[classes.index(tag)] = 1
        training.append(bag + output_row)

    random.shuffle(training)
    training = np.array(training)

    train_X, train_Y = training[:, :len(words)], training[:, len(words):]

    model = tf.keras.Sequential([
        # tf.keras.layers.Dense(1024, input_shape=(len(train_X[0]),), activation='relu'),
        # tf.keras.layers.BatchNormalization(),
        # tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(512, input_shape=(len(train_X[0]),), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(train_Y[0]), activation='softmax')
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.003)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    history = model.fit(train_X, train_Y, epochs=200, batch_size=64, verbose=1)

    model.save(MODEL_PATH)
    pickle.dump(history.history, open(HISTORY_PATH, 'wb'))
    print('Training complete!')

if __name__ == "__main__":
    train_chatbot(JSON_PATH)