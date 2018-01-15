import csv
import unidecode

arquivo_sujo='tweets_positivos.csv'
saida = open('tweets_positivos_1_coluna.txt','w')
with open(arquivo_sujo, 'r') as csvfile:
	arquivo = csv.reader(csvfile, delimiter='|')
	for row in arquivo:
		comment = row[0]
		unaccented_string = unidecode.unidecode(comment)
		comment = unaccented_string.lower()
		saida.write('"'+comment+'"\n')
saida.close()

