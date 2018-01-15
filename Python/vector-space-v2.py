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


def Phrase_to_Model(phrase):

	phrase_in_IQ = []
	phrase_in_model = {}
	for char in chars_to_remove:
		phrase=phrase.replace(char,' ')
	for char in chars_to_detect:
		phrase = phrase.replace(char,' '+char+' ')
	# phrase = phrase.replace('  ',' ')
	word_vector = phrase.split(' ')
	clean_word_vector = []

	word_vector = [word for word in word_vector if word not in STOPWORDS_DICT]
	word_quantity_in_phrase={}
	# considerando aqui que todas as palavras na frase serão utilizadas
	flag_next_is_first=1
	for word in word_vector:

		# if(phrase.index(word) ==0):
		# 	is_first = 1
		# ------------------------------
		# Analyse word for attributes:
		if word in chars_to_detect:
			flag_next_is_first = 1
			continue
		if flag_next_is_first:
			is_first = 1
			flag_next_is_first = 0

		isUpper = int(word.isupper())

		# --------------------

		word = word.lower()

		if(('aa' in word) or ('ee' in word) or ('ii' in word) or ('oo' in word) or ('uu' in word)):
			vowel_repeat = 1
		else:
			vowel_repeat = 0

		word = word.strip(' ')
		word = stemmer1.stem(word)
		if word == '':
			continue

		if word not in STOPWORDS:
			word_attribute_dict = {}
			if word in word_dict:
				word_dict[word] += 1
				# print('--:',word)
			else:
				word_dict[word] = 1
				# print('--:',word)
			if word in word_quantity_in_phrase:
				word_quantity_in_phrase[word] += 1
			else:
				word_quantity_in_phrase[word] = 1
			phrase_in_IQ+=[list(word_dict.keys()).index(word)]
			phrase_in_IQ+=[word_quantity_in_phrase[word]]
			print(word_quantity_in_phrase.keys())
			phrase_in_model[list(word_dict.keys()).index(word)]={'times':word_quantity_in_phrase[word],'UPPER':isUpper,'is_first':is_first,'vowel_repeat':vowel_repeat}
	# return phrase_in_IQ

	if not phrase_in_model:
		empty_phrase = {}
		empty_phrase[0]=0
		return empty_phrase
	else:
		return phrase_in_model
word_index = 0
phrase_list=[]
word_dict = OrderedDict()
word_dict['NULL**'] = 0


print('Going through lines in file, cleaning lines')
file_in=open(name_file_in,'r')

for line in tqdm(file_in):
	# print(line)

	phrase_in_vector = Phrase_to_Model(line)
	# phrase_list.append(Phrase_to_Model(line))
	phrase_list.append(phrase_in_vector)


little_ocourrences = [list(word_dict.keys()).index(word) for word in word_dict if word_dict[word] <= OCOURRENCES_MINIMUM]

final_matrix = []
old_matrix = []
# print(len(phrase_list))
print('Removing little accourrences...')
for phrase in tqdm(phrase_list,total=len(phrase_list)):
	new_line = []
	old_line = [0]*len(word_dict)

	for index in phrase:
		if index not in little_ocourrences:
			new_line +=[index]
			new_line +=[phrase[index]['times']]
			new_line +=[phrase[index]['UPPER']]
			new_line +=[phrase[index]['is_first']]
			new_line +=[phrase[index]['vowel_repeat']]
			old_line[index] = phrase[index]['times']
	final_matrix.append(new_line)
	old_matrix.append(old_line)

print('Writing result in file...')
with open(name_file_in+'_out_file','w') as out_file:
	spamwriter = csv.writer(out_file, delimiter=' ')
	for row in tqdm(final_matrix, total=len(final_matrix)):
		if not row:
			row = [0,0,0,0,0]
		spamwriter.writerow(row)
with open(name_file_in+'_out_file_old_model','w') as out_file:
	spamwriter = csv.writer(out_file, delimiter=' ')
	for row in tqdm(old_matrix, total=len(old_matrix)):
		spamwriter.writerow(row)
print('Writing word list...')
print(len(word_dict))
with open(name_file_in+'_word_list','w') as word_list_file:
	for word in word_dict:
		word_list_file.write(word+'\n')


print('Writing clean sentences file...')

with open(name_file_in+'_clean_sentences','w') as clean_sentences_file:
	for phrase in tqdm(phrase_list,total=len(phrase_list)):
		line = ''
		ordered_word_list = list(word_dict.keys())
		for index in phrase:
			if index not in little_ocourrences:
				line +=ordered_word_list[index]
				line +=' '
		clean_sentences_file.write(line+'\n')

print('Done!!')





# = [word for word in word_vector if word not in nltk.corpus.stopwords.words(language)]
# everything_in_a_phrase = " ".join(phrase_list)

# tokens = nltk.word_tokenize(everything_in_a_phrase)
# fdist=FreqDist(tokens)
# to_remove=list(filter(lambda x: x[1]<=5,fdist.items()))
# print(len(to_remove))

# phrase_list_1 = []
# for phrase in phrase_list:
# 	words =phrase.split(' ')
# 	words_2=[]
# 	for word in words:
# 		if word not in to_remove:
# 			words_2.append(word)

# 	phrase_1 = ' '.join(words_2)
# 	phrase_list_1.append(phrase_1)




# phrase_list_1 = phrase_list
# vectorizer = CountVectorizer()


# vectorizer.fit(phrase_list_1)


# corpus_vec = vectorizer.transform(phrase_list_1).toarray()


# with open('out_file'+name_file_in+'2.csv','w') as out_file:
# 	print('Writing Lines...')
# 	for line in tqdm(corpus_vec,total = len(corpus_vec)):
# 		# print(len(line))
# 		for item in line:
# 			out_file.write(str(item)+' ')
# 		out_file.write('\n')