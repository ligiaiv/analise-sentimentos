import sys
from tqdm import tqdm
###Classes prp - preposição
#	 		art - artigo
#			adj - adjetivo
#			num - numeral
# 			n   - substantivo
###
try:
	name_file_in = sys.argv[1]
	name_file_out = sys.argv[2]
	classes_to_leave = sys.argv[3:len(sys.argv)]
	print(classes_to_leave)
except Exception as e:
	print('Use: File_in File_out class1 class2 ... ')
	exit()

classes_to_leave.extend(['.','?','!'])


file_in = open(name_file_in,'r')
file_out = open(name_file_out,'w')
line_list=[]
problem_lines = 0
for line in tqdm(file_in):
	words = line.split('|')
	new_line = []
	line_string = ''
	for word in words:
		word=word.replace(']','[')
		itens = word.split('[')

		try:
			original = itens[0]
			base = itens[1]
			classe = itens[2].strip('\n').strip(' ')
			# print(classe)
		except Exception as e:
			# print(word)
			problem_lines+=1
		if 'v-' in classe:
			classe ='v'
		if base is '':
			base = original
		if classe in classes_to_leave:
			new_line.append(base)
			line_string = line_string+base+' '
	# if line_string is not '':
	file_out.write(line_string+'\n')
print(problem_lines)
file_in.close()
file_out.close()
