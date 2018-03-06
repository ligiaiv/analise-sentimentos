import sys
from tqdm import tqdm

POSITIVE_EMOJI=[':)', ':-)',':3','=)',':D','xD','XD','=3']
NEGATIVE_EMOJI=[':(', ':-(',':/',':\\',':c',":'(",'=/','=\\']
try:
	name_file_in = sys.argv[1]
	name_file_out = sys.argv[2]
except Exception as e:
	print('Name of file needed. ')
	exit()
# name_file_out =name_file_in.split('/')
# name_file_out[0]='out_files'
# name_file_out[-1]+='_out_files'
# name_file_out='/'.join(name_file_out)
frase_list=[]
with open(name_file_in,'r') as original_file:
#	temp_dict = {	"phrase":phrase,
#					"positive":0,
#					"negative":0
#				}
	for phrase in tqdm(original_file):
		phrase=phrase.replace('\n','').replace('"','').replace('http://','  ').replace('https://','  ').replace('http:/','  ').replace('https:/','  ')
		positive_score=0
		negative_score=0
		for emoji in POSITIVE_EMOJI:
			if emoji in phrase:
				# print('oiii')
				positive_score=1
				continue
		for emoji in NEGATIVE_EMOJI:
			if emoji in phrase:
				negative_score=1
				continue
		if positive_score == 0 and negative_score == 0:
			frase_list.append(phrase)
with open(name_file_out,'w') as out_file:
	for phrase in frase_list:
		out_file.write(phrase+'\n')



