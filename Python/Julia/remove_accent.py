import csv
import unidecode
import sys
if len(sys.argv) != 3:
	print('You used '+str(len(sys.argv)-1)+' argumens. 2 necessary')
	print('Usage: python remove_accent.py accented_file output_file')
	exit()
arquivo_sujo= sys.argv[1]
saida = open(sys.argv[2],'w')

with open(arquivo_sujo, 'r') as file:
	for linha in file:
		unaccented_string = unidecode.unidecode(linha)
		saida.write(unaccented_string+'\n')
saida.close()
print('Done removing accents')
