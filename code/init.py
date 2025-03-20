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
	if isinstance(text_input, list):
		text_input = " ".join(text_input)

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