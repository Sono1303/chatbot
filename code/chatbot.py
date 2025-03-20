import random
import json
import re
import pickle
import numpy as np
from init import lemmatizer, extract_ingredients
from neural_based_chatbot import JSON_PATH, WORDS_PATH, CLASSES_PATH, MODEL_PATH
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  
from keras.models import load_model

intents = json.load(open(JSON_PATH))
intents_dict = {intent['tag']: intent for intent in intents['intents']} 
words = pickle.load(open(WORDS_PATH, 'rb'))
classes = pickle.load(open(CLASSES_PATH, 'rb'))
model = load_model(MODEL_PATH)

last_user_input = None
list_optimal_choice = None
last_optimal_choice = None

# # Normalize words to their original form
# def clean_up_sentence(sentence):
# 	sentence = sentence.lower() # Lower characters
# 	sentence = re.sub(r"[^a-zA-Z0-9\s]", "", sentence) # Keep letters and numbers

# 	return [lemmatizer.lemmatize(word) for word in nltk.word_tokenize(sentence)]

# Vectorize sentence
def bag_of_words(sentence):
	sentence_words = extract_ingredients(sentence)
	return np.array([1 if word in sentence_words else 0 for word in words])

# Predict class
def predict_class(sentence):
	bow = bag_of_words(sentence) 
	res = model.predict(np.array([bow]))[0] 
	ERROR_THRESHOLD = np.median(res) # Use mean of predict array for threshold

	results = sorted(
		[[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD],
		key=lambda x:x[1],
		reverse=True
	) # Sort the results in descending order of probability

	return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results] # return list of classes and their probability

# Get Optimal choice based on probability and match score
def get_optimal_choice(sentence, intents_list):
	global last_user_input, list_optimal_choice, last_optimal_choice

	if last_user_input == sentence:	
		list_optimal_choice = [choice for choice in list_optimal_choice if choice[0] != last_optimal_choice]
	else:
		ingredients = set(extract_ingredients(sentence))
		optimal_choices = []
		for choice in intents_list:
			intent = intents_dict.get(choice['intent'])
			if not intent:
				continue

			list_ingredient = intent['patterns']
			if not list_ingredient:
				continue

			count = sum(1 for ingredient in list_ingredient if ingredient in ingredients)
			if count == 0:
				continue
			if count == len(ingredients):
				match_score = (count / len(list_ingredient)) + 1
			else:
				match_score = count / len(list_ingredient)
			optimal_choices.append((choice['intent'], match_score))

		if not optimal_choices:
			return None
		
		list_optimal_choice = sorted(optimal_choices, key=lambda x: x[1], reverse=True)
	
	if not list_optimal_choice:
		return None
	# print(list_optimal_choice)
	optimal_choice = list_optimal_choice[0][0]

	last_user_input = sentence
	last_optimal_choice = optimal_choice

	return optimal_choice

def get_response(sentence):
	global last_user_input

	intents_list = None

	if last_user_input != sentence:
		intents_list = predict_class(sentence)

	tag = get_optimal_choice(sentence, intents_list)

	if tag:
		intent = intents_dict.get(tag)
		if intent:
			text = intent['responses'] if isinstance(intent['responses'], str) else random.choice(intent['responses'])
			response = {'text': text} # Return text
			if "image" in intent:
				response['image'] = intent['image'] # Return text and image (if image available)
			return response
	return {'text':"Sorry, can you ask me again?" }

if __name__ == "__main__":
    print("Chatbot is running! Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ["exit", "quit", "bye"]:
            print("Bot: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print("Bot:", response)