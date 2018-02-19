import csv
import unidecode,codecs
import sys,tqdm
try:
	name_file_in = sys.argv[1]
	name_file_out = name_file_in.replace('datasets','out_files')
	column_i_want = int(sys.argv[2])
	if column_i_want <=0:
		# print('oi ',sys.argv)
		print('Column index starts at 1. ')
		exit()
except Exception as e:
	print('Name of file and number of column needed. ')
	exit()


arquivo_sujo='tweets_positivos.csv'
saida = codecs.open(name_file_in+'_CIW','w',)
with codecs.open(name_file_in, 'r') as csvfile:
	arquivo = csv.reader(csvfile, delimiter='|')
	lines_read=0
	for row in arquivo:
		lines_read+=1
		# sys.stdout.flush()
		# sys.stdout.write("Lines read: %d   \r" % (lines_read) )
		print(lines_read)
		comment = row[column_i_want-1].replace('"','')
		unaccented_string = unidecode.unidecode(comment)
		comment = unaccented_string.lower()
		saida.write('"'+comment+'"\n')
saida.close()

