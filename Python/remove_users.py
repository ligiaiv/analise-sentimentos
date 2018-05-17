import sys
try:
	name_file_in = sys.argv[1]
	name_file_out = sys.argv[2]
except Exception as e:
	print('Name of file needed. ')
	exit()


file_out = open(name_file_out,'w')
with open(name_file_in,'r') as file_in:
	for line in file_in:
		new_line = ''
		words = line.split(' ')
		for word in words:
			if '@' in word:
				new_word = " "
				if '.' in word:
					new_word = '.'

				if '!' in word:
					new_word = '!'
				if '?' in word:
					new_word = '?'
				new_line = new_line+new_word
		file_out.write(new_line+'')
file_out.close()
