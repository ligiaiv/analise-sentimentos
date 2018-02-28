import csv
import unidecode,codecs
import sys,tqdm
delimiter = '|'
try:
	name_file_in = sys.argv[1]
	name_file_out = sys.argv[2]
	column_i_want = int(sys.argv[3])
	if column_i_want <=0:
		# print('oi ',sys.argv)
		print('Column index starts at 1. ')
		exit()
except Exception as e:
	print('Use:   Name_file_in   Name_file_out   id_column ')
	exit()


arquivo_sujo='tweets_positivos.csv'
saida = open(name_file_out,'w',)
with open(name_file_in, 'r') as arquivo:
	# arquivo = csv.reader(csvfile, delimiter='|')
	lines_read=0
	for linha in arquivo:
		row = linha.strip('\n').split(delimiter)
		lines_read+=1
		sys.stdout.flush()
		sys.stdout.write("Lines read: %d   \r" % (lines_read) )
		# print(lines_read)
		comment = row[column_i_want-1].replace('"','')
		unaccented_string = unidecode.unidecode(comment)
		comment = unaccented_string.lower()
		saida.write('"'+comment+'"\n')
saida.close()

