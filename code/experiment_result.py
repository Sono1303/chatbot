import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import numpy as np
from keras.models import load_model

history = pickle.load(open('model/history.pkl', 'rb'))

final_accuracy = history['accuracy'][-1]
print(f'Final Training Accuracy: {final_accuracy:.4f}')

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history['loss'], label='Train Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Loss Over Time')

plt.subplot(1, 2, 2)
plt.plot(history['accuracy'], label='Train Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Accuracy Over Time')

plt.show()

