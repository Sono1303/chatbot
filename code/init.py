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
	single_nouns = [lemmatizer.lemmatize(word) for word, pos in pos_tags if pos.startswith("NN") and word not in extracted_words]

	return ingredients + single_nouns