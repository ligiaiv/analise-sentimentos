import pandas as pd
import nltk
import nltk.stem
import bisect
import re
from nltk import FreqDist

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint
LANGUAGE = 'english'
chars_to_remove = [',',';',':','"',"'",'\n','\t']

class WordNetStemmer(WordNetLemmatizer):
    def stem(self,word,pos=u'n'):
        return self.lemmatize(word,pos)

class Stemmer(object):
    def __init__(self,stemmer_type):
        self.stemmer_type = stemmer_type
        if (self.stemmer_type == 'porter'):
            self.stemmer = nltk.stem.PorterStemmer()
        elif (self.stemmer_type == 'snowball'):
            self.stemmer = nltk.stem.SnowballStemmer(LANGUAGE)  #<<<----------------VER SE TEM EM PORTUGUES
        elif (self.stemmer_type == 'lemmatize'):
            self.stemmer = WordNetStemmer()
        else:
            raise NameError("'"+stemmer_type +"'" + " not supported")
# -------------------------------------------------------------

# creates stemmer to normalize words, types possiblle: porter, snowball, lemmatize, this last one needs information about the class of the word
stemmer1 = Stemmer('snowball').stemmer



file_frases = 'inputs/neg'
file_pesos = 'inputs/teste1.xlsx'


# Le o arquivo de pesos e cria um dicionário
def read_pesos(file_pesos):
	df = pd.DataFrame()
	if '.xls' in file_pesos:
		df = pd.read_excel(file_pesos)

	else:
		df = pd.read_csv(file_pesos)
	word_dict = dict(zip(df.iloc[:,0],df.iloc[:,1]))
	return word_dict

def read_frases(file_frases):
	with open(file_frases,'r') as f:
		frase_list = f.read().splitlines()
	return frase_list

word_dict = read_pesos(file_pesos)

frase_list = read_frases(file_frases)
pprint(frase_list)
values_list = []
for line in frase_list:
	line=re.sub("|".join(chars_to_remove), " ", line)
	line = line.split(' ')
	line = [word_dict.get(x) for x in line]

	line = [0 if x == None else x for x in line]
	value = sum(line)
	values_list.append(value)
out_df = pd.DataFrame({
		'Frase':frase_list,
		'Valores':values_list
	})
if 'xls' in file_pesos:
	writer = pd.ExcelWriter('file_frases'.split('.')[0]+'xlsx')
	out_df.to_excel(writer)
	writer.save()
	# out_df.to_excel('file_frases'.split('.')[0]+'xlsx')
else:
	out_df.to_csv('file_frases'.split('.')[0]+'csv')
