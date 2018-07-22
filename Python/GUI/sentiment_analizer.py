import pandas as pd
import numpy as np
import nltk
import nltk.stem
import bisect
import re
import time
from nltk import FreqDist

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint
from operator import methodcaller
LANGUAGE = 'portuguese'
SENTIMENT_DIM = 0
chars_to_remove = [',',';',':','"',"'",'!','.','\n','\t']
HEADER_LIST = []
FRASES = []
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


# Le o arquivo de pesos e cria um dicionário
def read_pesos(file_pesos):
	global SENTIMENT_DIM, HEADER_LIST
	print(file_pesos)
	print('HERE')

	df = pd.DataFrame()
	if '.xls' in file_pesos:
		df = pd.read_excel(file_pesos)

	else:
		df = pd.read_csv(file_pesos)

	HEADER_LIST = list(df)

	df_weights = df.iloc[:,1:]
	SENTIMENT_DIM = df_weights.shape[1]
	print(SENTIMENT_DIM)
	word_dict = dict(zip(df.iloc[:,0],	np.array(df_weights.values)))
	pprint(word_dict)
	return word_dict

def read_frases(file_frases):

	global FRASES
	with open(file_frases,'r') as f:
		frase_list = f.read().splitlines()
		FRASES = frase_list.copy()

		pprint(frase_list)
		# subj.translate(None, ''.join(chars_to_remove))
		frase_list = [re.sub('['+(''.join(chars_to_remove))+']','',frase) for frase in frase_list]

		# frase_list = list(map(methodcaller("translate", None,''.join(chars_to_remove)), frase_list))		

		# frase_list = list(map(lambda x: re.sub("|".join(chars_to_remove), " ", x), frase_list))
		# frase_list = list(map(re.sub("|".join(chars_to_remove), " ", line), frase_list))		

		frase_list = list(map(methodcaller("split", " "), frase_list))		
		pprint(frase_list)
	return frase_list


def process(file_frases,file_pesos,outfile,export_format,language):

	if language == "portuguese":
		stemmer = nltk.stem.RSLPStemmer()
	elif language == "english":
		stemmer = nltk.stem.porter.PorterStemmer()
	# stemmer1 = Stemmer('snowball').stemmer

	# file_frases = 'inputs/frases.txt'
	# file_pesos = 'inputs/teste1.xlsx'

	word_dict = read_pesos(file_pesos)

	frase_list = read_frases(file_frases)
	pprint(frase_list)
	values_list = []
	for line in frase_list:
		# line=re.sub("|".join(chars_to_remove), " ", line)
		# line = line.split(' ')
		line = list(map(stemmer.stem, line))
		print(line)	
		line = np.array([word_dict.get(x,np.zeros(SENTIMENT_DIM)) for x in line])
		# print(line)
		# # line = np.array(line)
		# line = np.array( line )
		print(line)
		# line[line==None] = np.zeros(SENTIMENT_DIM)
		# line = [0 if x == None else x for x in line]
		line = np.sum(line,axis = 0)
		print(line)
		# value = sum(line)
		values_list.append(line)
	out_df = pd.DataFrame(data = values_list,columns = HEADER_LIST[1:])
	out_df.insert(0,HEADER_LIST[0],FRASES)
	# out_df = pd.DataFrame({
	# 		'Frase':frase_list,
	# 		'Valores':values_list
	# 	})
	if 'EXCEL' in export_format:
		writer = pd.ExcelWriter(outfile+'.xlsx',engine='xlsxwriter')
		out_df.to_excel(writer)
		writer.save()
		# out_df.to_excel('file_frases'.split('.')[0]+'xlsx')
	else:
		
		out_df.to_csv(outfile+'.csv')
	return('OK')

