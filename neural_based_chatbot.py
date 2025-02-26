import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

with open('intents.json') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_chars = {'?', '!', '.', ','}

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set(lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars))
classes = sorted(set(classes))

pickle.dump(words, open('model/words.pkl', 'wb'))
pickle.dump(classes, open('model/classes.pkl', 'wb'))

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

model.fit(train_X, train_Y, epochs=500, batch_size=16, verbose=1)

model.save('model/chatbot_model.keras')
print('Training complete!')