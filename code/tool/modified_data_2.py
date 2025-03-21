import json 
import nltk
from nltk import pos_tag, word_tokenize
from nltk.chunk import RegexpParser
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Uncomment and download if first time run code
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger_eng")
# nltk.download('wordnet')

def extract_ingredients(text_input):
	base = len(text_input)
	if isinstance(text_input, list):
		text_input = ",".join(text_input)
	
	words = word_tokenize(text_input)
	
	pos_tags = pos_tag(words)
	# print(pos_tags)
	pos_tags = [(lemmatizer.lemmatize(word, 'n') if pos in ['NNS','VBZ']  else word, 'NN' if pos in ['NNS','VBZ'] else pos) for word, pos in pos_tags]
	# print(pos_tags)
	# grammar = r"""
	# 	NP: {<VBP><JJ>}
    #         {<NN><POS><NN>*<NN>}
	# 		{<JJ|VBD|VBN|NN>+<NN>}   
	# 		{<NN><NN>}         	
	# 		{<JJ>}
	# 		{<FW>}
	# 		{<PRP>}
	# 		{<IN><NN>}
	# 		{<RB><NN>}
	# 		{<NN>*<RB>}
	# 		{<NN>}
	# """
	grammar = r"""
    NP: {<NN><POS><NN>*<NN>}         # Noun phrase with possessive (e.g., John's book)
        {<VBP><JJ>}                  # Verb in present tense + Adjective (e.g., is beautiful)
        {<JJ|VBD|VBN|NN>+<NN>}       # Adjectives or past tense + Noun
        {<NN><NN>}                   # Noun + Noun (e.g., rice cooker)
        {<IN><NN>}                   # Preposition + Noun (e.g., in kitchen)
        {<RB><NN>}                   # Adverb + Noun (e.g., very rice)
        {<NN>*<RB>}                  # Noun + Adverb (e.g., food well)
        {<JJ>}                       # Single Adjective
        {<FW>}                       # Foreign Word
        {<PRP>}                      # Pronoun
        {<NN>}                       # Single Noun
	"""


	chunk_parser = RegexpParser(grammar)
	tree = chunk_parser.parse(pos_tags)

	ingredients = [" ".join(word for word, pos, in subtree.leaves())
				   for subtree in tree if isinstance(subtree, nltk.Tree)]
	extracted_words = set(word for phrase in ingredients for word in phrase.split())
	single_nouns = [word for word, pos in pos_tags if pos.startswith("NN") and word not in extracted_words]

	return ingredients + single_nouns#, base, len(ingredients + single_nouns)

# print(extract_ingredients([
#                 "boiled egg",1
#                 "chili powder",2
#                 "chicken",3
#                 "coriander",4
#                 "fish sauce",5
#                 "garlic",6
#                 "lime",7
#                 "rice noodles",8
#                 "salt",9
#                 "shallots",
#                 "turmeric",
#                 "vegetable oil"
#             ]))

def modified_data_2(data_input):
	data = json.load(open(data_input))
	# print(data)
	modified_data = []
	fail_modified = []
	for item in data['intents']:
		tmp = item
		base_len = len(item['patterns'])
		data_base = item['patterns']
		tmp['patterns'] = extract_ingredients(item['patterns'])
		after_len = len(tmp['patterns'])
		data_after = tmp['patterns']
		
		modified_data.append(tmp)
		if base_len != after_len:
			print(data_base)
			print(data_after)
			fail_modified.append((tmp['tag'], after_len,base_len))

	modified_json = {
		"intents": modified_data
	}

	with open(data_input, 'w') as f:
		json.dump(modified_json, f, indent=4)
	print(fail_modified)
	print(len(fail_modified))
	print("Done modified data 2")

INPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\ing.json'
OUTPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'

if __name__ == '__main__':
    modified_data_2(OUTPUT_PATH)