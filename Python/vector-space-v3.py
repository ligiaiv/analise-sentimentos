import nltk
import nltk.stem
from nltk import FreqDist

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

from collections import OrderedDict
from stopwords import STOPWORDS



import re, unidecode,csv
from tqdm import tqdm
import sys
language = 'english'
OCOURRENCES_MINIMUM = 5
# -------------------------------------------------------------
#  tem que colocar essa parte pra funcionar depois o stemmer
# ----------------

if language is 'portugese':
	STOPWORDS_DICT = STOPWORDS
else:
	STOPWORDS_DICT=nltk.corpus.stopwords.words(language)
chars_to_remove = [',',';',':','"',"'",'\n','\t']
chars_to_detect = ['.','!','?',]
NEGATIVE_WORDS={
				'portuguese':['não','nunca','jamais'],
				'english':['no',"don't","doesn't",'never','not']
				}

class WordNetStemmer(WordNetLemmatizer):
    def stem(self,word,pos=u'n'):
        return self.lemmatize(word,pos)

class Stemmer(object):
    def __init__(self,stemmer_type):
        self.stemmer_type = stemmer_type
        if (self.stemmer_type == 'porter'):
            self.stemmer = nltk.stem.PorterStemmer()
        elif (self.stemmer_type == 'snowball'):
            self.stemmer = nltk.stem.SnowballStemmer(language)  #<<<----------------VER SE TEM EM PORTUGUES
        elif (self.stemmer_type == 'lemmatize'):
            self.stemmer = WordNetStemmer()
        else:
            raise NameError("'"+stemmer_type +"'" + " not supported")
# -------------------------------------------------------------

# creates stemmer to normalize words, types possiblle: porter, snowball, lemmatize, this last one needs information about the class of the word
stemmer1 = Stemmer('snowball').stemmer
stopwords = nltk.corpus.stopwords.words(language)


try:
	name_file_in = sys.argv[1]
except Exception as e:
	print('Name of file needed. ')
	exit()

word_dict = OrderedDict()


# Get one Phrase and returns vector
def Phrase_to_Model(phrase):
	negative_positions = []
	phrase_model = {}
	f_next_is_first = 1
	phrase_words_in_dict={}
	clean_phrase=[]
	for word in phrase:
		if (word not in STOPWORDS) and (word not in chars_to_remove):
			clean_phrase.append(word)
	phrase = clean_phrase
	for word in phrase:
		f_upper = int(word.isupper())

		if(f_next_is_first):
			f_is_first = 1
			f_next_is_first=0
		else:
			f_is_first=0

		if word in chars_to_detect:
			f_next_is_first=1
			continue

		temp_word = word.lower()
		if(('aa' in temp_word) or ('ee' in temp_word) or ('ii' in temp_word) or ('oo' in temp_word) or ('uu' in temp_word)):
			vowel_repeat = 1
		else:
			vowel_repeat = 0

		if temp_word in NEGATIVE_WORDS[language]:
			f_is_negative = 1;
			negative_positions.append(phrase.index(temp_word));
		# get sistance from negative word
		# else:
		# 	distance_from_negative = 	

		word = word.strip(' ')
		word = stemmer1.stem(word)

		if word not in STOPWORDS:
			if word not in word_dict:
				word_dict[word]=1
			else:
				word_index = list(word_dict.keys()).index(word)
				if word_index not in phrase_model:
					word_dict[word]+=1
	
			# Construct Phrase Model
			word_index = list(word_dict.keys()).index(word)
			word_info={'IS_FIRST':f_is_first,
						'UPPER':f_upper,
						'VOWEL_REPEAT':vowel_repeat,
						'IS_NEGATIVE':f_is_negative
					}
			phrase_words_in_dict[word_index]=word_info

			# phrase_model.extend([word_index,f_is_first,f_upper,vowel_repeat,f_is_negative])



