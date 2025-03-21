import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pickle
import json
import random
import nltk 
from nltk import pos_tag, word_tokenize
from nltk.chunk import RegexpParser
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger_eng")

JSON_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'
MODEL_PATH = r"E:\Chatbot\Neural_network_chatbot\model\chatbot_bert.keras"
BERT_MODEL = r"https://tfhub.dev/google/universal-sentence-encoder/4"
LABEL_PATH = r"E:\Chatbot\Neural_network_chatbot\model\label_encoder.pkl"

intents = json.load(open(JSON_PATH))
intents_dict = {intent['tag']: intent for intent in intents['intents']} 
model = tf.keras.models.load_model(MODEL_PATH)
bert_layer = hub.KerasLayer(BERT_MODEL, trainable=False)
label_encoder = pickle.load(open(LABEL_PATH, "rb"))

last_user_input = None
list_optimal_choice = None
last_optimal_choice = None

def extract_ingredients(text_input):
	words = word_tokenize(text_input)
	pos_tags = pos_tag(words)

	grammar = r"""
		NP: {<JJ|VBD|VBN>*<NN>}   
			{<NN><NN>}         
	"""

	chunk_parser = RegexpParser(grammar)
	tree = chunk_parser.parse(pos_tags)

	ingredients = [" ".join(word for word, pos, in subtree.leaves())
				   for subtree in tree if isinstance(subtree, nltk.Tree)]

	extracted_words = set(word for phrase in ingredients for word in phrase.split())
	single_nouns = [lemmatizer.lemmatize(word) for word, pos in pos_tags if pos.startswith("NN") and word not in extracted_words]

	return ingredients + single_nouns

def get_optimal_choice(text_input, prediction):
	global last_user_input, list_optimal_choice, last_optimal_choice

	if last_user_input == text_input:	
		list_optimal_choice = [choice for choice in list_optimal_choice if choice[1] != last_optimal_choice]
	else:
		ingredients = set(extract_ingredients(text_input))
		optimal_choices = []

		for choice in prediction:
			tag = label_encoder.inverse_transform([choice[0]])[0]
			
			intent = intents_dict.get(tag)
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
			optimal_choices.append([choice[0], tag, match_score])

		if not optimal_choices:
			return None
		
		list_optimal_choice = sorted(optimal_choices, key=lambda x: x[2], reverse=True)
	
	if not list_optimal_choice:
		return None
	# print(list_optimal_choice)
	optimal_choice = list_optimal_choice[0][1]

	last_user_input = text_input
	last_optimal_choice = optimal_choice

	return optimal_choice

def get_predict(text_input):
	embedding = np.array(bert_layer([text_input]))
	prediction = model.predict(embedding)
	threshold = np.median(prediction[0])
	
	results = sorted(
		[(idx, prob) for idx, prob in enumerate(prediction[0]) if prob >= threshold],
		key=lambda x: x[1],
		reverse=True
	)
	
	return results

# def get_optimal_choice(text_input):

def get_response(text_input):
	global last_user_input

	prediction = None
	
	if last_user_input != text_input:
		prediction = get_predict(text_input)

	predicted_tag = get_optimal_choice(text_input, prediction)

	if predicted_tag:
		intent = intents_dict.get(predicted_tag)
		if intent:
			text = intent['responses'] if isinstance(intent['responses'], str) else random.choice(intent['responses'])
			response = {'text': text} # Return text
			if "image" in intent:
				response['image'] = intent['image'] # Return text and image (if image available)
			return response
		
	return {'text': "Sorry, can you ask me again?"}

print(get_response("cooked rice, egg"))

# text = "Hi"
# response = get_response(text, model, bert_layer, intents_dict)
# print("Chatbot:", response)

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Goodbye!")
#         break
#     response = get_response(user_input)
#     print("Chatbot:", response)
