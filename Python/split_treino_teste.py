import sys
try:
	name_file_in_pos = sys.argv[1]
	name_file_in_neg = sys.argv[2]
	name_file_out = sys.argv[3]

	# name_file_out = sys.argv[2]
	# classes_to_leave = sys.argv[3:len(sys.argv)]
	# print(classes_to_leave)
except Exception as e:
	print(e)
	print('Use: File_in_positiva File_in_negativa ')
	exit()

frases_positivas = []
frases_negativas = []

with open(name_file_in_pos,'r') as file_in_pos:
	for line in file_in_pos:
		frases_positivas.append(line)

with open(name_file_in_neg,'r') as file_in_neg:
	for line in file_in_neg:
		frases_positivas.append(line)

pos_len = len(frases_positivas)

neg_len = len(frases_negativas)

with open(name_file_out+'_treino','w') as file_out:
	for line in frases_positivas[:(pos_len//2)]:
		file_out.write(line);
	for line in frases_negativas[:(neg_len//2)]:
		file_out.write(line);

with open(name_file_out+'_teste','w') as file_out:
	for line in frases_positivas[(pos_len//2):]:
		file_out.write(line);
	for line in frases_negativas[:(neg_len//2):]:
		file_out.write(line);

with open(name_file_out+'_treino_score','w') as file_out:
	for line in frases_positivas[:(pos_len//2)]:
		file_out.write("1\n");
	for line in frases_negativas[:(neg_len//2)]:
		file_out.write("-1\n");

with open(name_file_out+'_teste_score','w') as file_out:
	for line in frases_positivas[(pos_len//2):]:
		file_out.write("1\n");
	for line in frases_negativas[:(neg_len//2):]:
		file_out.write("-1\n");
