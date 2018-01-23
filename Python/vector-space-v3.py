import nltk
import nltk.stem
import bisect
from nltk import FreqDist

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

from collections import OrderedDict
from stopwords import STOPWORDS



import re, unidecode,csv
from tqdm import tqdm
import sys
language = 'english'
OCOURRENCES_MINIMUM = 3
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
	# remove stop words


	for word in phrase:
		word = word.strip(' ')
		word = stemmer1.stem(word)
		if (word not in STOPWORDS) and (word not in chars_to_remove) or (word in NEGATIVE_WORDS[language] ):
			clean_phrase.append(word)
	phrase = clean_phrase

	#
	for word in phrase:
		if word is '':
			continue
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



		f_is_negative=0
		if temp_word in NEGATIVE_WORDS[language]:
			f_is_negative = 1;
			negative_positions.append(phrase.index(temp_word));
		# get sistance from negative word
		# else:
		# 	distance_from_negative =


		if (word not in STOPWORDS) or (word in NEGATIVE_WORDS[language]) :
			if word not in word_dict:
				word_dict[word]=1
			else:
				word_index = list(word_dict.keys()).index(word)+1
				if word_index not in phrase_model:
					word_dict[word]+=1

			# Construct Phrase Model
			word_index = list(word_dict.keys()).index(word)+1
			word_info={	'WORD':word,
						'IS_FIRST':f_is_first,
						'UPPER':f_upper,
						'VOWEL_REPEAT':vowel_repeat,
						'IS_NEGATIVE':f_is_negative,
						'WORD_INDEX': word_index
					}
			phrase_words_in_dict[phrase.index(temp_word)]=word_info

			# phrase_model.extend([word_index,f_is_first,f_upper,vowel_repeat,f_is_negative])
	# FIND DISTANCE to NEGATIVE WORD
	for word_position,word_info in phrase_words_in_dict.items():
		# if len(negative_positions) != 0:

		# 	min_distance=500
		# 	for neg_word in negative_positions:
		# 		distance=abs(neg_word-word_position)
		# 		if distance < min_distance:
		# 			min_distance=distance
		# 	# distance = min(abs(negative_positions-word_info['POSITION_IN_PHRASE']))
		# 	phrase_words_in_dict[word_position]['DISTANCE_TO_NEGATIVE']=min_distance
		# else:
		# 	phrase_words_in_dict[word_position]['DISTANCE_TO_NEGATIVE']=0
		i = bisect.bisect_left(negative_positions,word_position)
		distance=0
		if(i < len(negative_positions)):
			distance = negative_positions[i]-word_position

		phrase_words_in_dict[word_position]['DISTANCE_TO_NEGATIVE']=distance


	return phrase_words_in_dict
	# return_vector=[]
	# for index,word_info in phrase_words_in_dict.items():
	# 	return_vector.extend([index,word_info['IS_FIRST'],word_info['UPPER'],word_info['VOWEL_REPEAT'],word_info['IS_NEGATIVE'],word_info['DISTANCE_TO_NEGATIVE']])
	# return return_vector


#################################################################
#																#
#		MAIN 													#
#																#
#################################################################

# name_file_out = '/'.join((name_file_in.split('/').pop(0)).insert(0,'out_files').insert(-1,'out_file'))
name_file_out =name_file_in.split('/')
name_file_out[0]='out_files'
# name_file_out[-1]+='_out_files'
name_file_out='/'.join(name_file_out)
print('Going through lines in file, cleaning lines')
phrase_list=[]
file_in=open(name_file_in,'r')
for line in tqdm(file_in):
	# print(line)
	phrase = line
	for char in chars_to_remove:
		phrase=phrase.replace(char,' ')
	for char in chars_to_detect:
		phrase = phrase.replace(char,' '+char+' ')
	# phrase = phrase.replace('  ',' ')
	word_vector = phrase.split(' ')
	phrase_list.append(Phrase_to_Model(word_vector))

# REMOVING LITTLE OCCURRENCES and writing to model
print('Removing little occurrences...')

little_occurrences = [list(word_dict.keys()).index(word)+1 for word in word_dict if word_dict[word] < OCOURRENCES_MINIMUM]

final_matrix=[]
# print(phrase_list)
for phrase in tqdm(phrase_list, total=len(phrase_list)):
	phrase_vector=[]

	for position,word in phrase.items():

		if word['WORD_INDEX'] not in little_occurrences:
			phrase_vector.extend([word['WORD_INDEX'],word['IS_FIRST'],word['UPPER'],word['VOWEL_REPEAT'],word['IS_NEGATIVE'],word['DISTANCE_TO_NEGATIVE']])
	final_matrix.append(phrase_vector)


print('Writing result in file...')
with open(name_file_out+'_OUT_FILE','w') as out_file:
	spamwriter = csv.writer(out_file, delimiter=' ')
	for row in tqdm(final_matrix, total=len(final_matrix)):
		if not row:
			row = [0,0,0,0,0,0]
		spamwriter.writerow(row)

print('Writing word list...')
with open(name_file_out+'_WORD_LIST','w') as word_list_file:
	for word in word_dict:
		if word != '':
			word_list_file.write(word+'\n')
