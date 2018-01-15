import json

sentiment_dict = {}
to_remove = set()
repeated = []
to_remove_duplicates = []
in_file = 'emolexDictionaryPort.txt'
f_out = open('emolexDictionaryPort_clean.txt','w')
f_log = open('log.txt','w')
with open(in_file) as f_in:
	for line in f_in:
		word = line.split()[0].lower()
		sentiment_type = line.split()[-2]
		sentiment_value = line.split()[-1]

		if word not in sentiment_dict:
			sentiment_dict[word]={
								  # 'count':0,
								  'anger':[],
								  'anticipation':[],
								  'disgust':[],
								  'fear':[],
								  'joy':[],
								  'negative':[],
								  'positive':[],
								  'sadness':[],
								  'surprise':[],
								  'trust':[]
								}

		# sentiment_dict[word]['count']=sentiment_dict[word]['count']+1
		sentiment_dict[word][sentiment_type].append(sentiment_value)


for word,sentiments in sentiment_dict.items():
	for sentiment_type, values_vector in sentiments.items():
		if len(list(set(values_vector)))>1:
			to_remove.add(word)
			# del sentiment_dict[word]
for word in to_remove:
	del sentiment_dict[word]

for word,sentiments in sorted(sentiment_dict.items()):
	for sentiment_type, values_vector in sorted(sentiments.items()):
		f_out.write(word+'\t'+sentiment_type+'\t'+values_vector[0]+'\n')
	# del sentiment_dict[word]['count']
	# for sentiment_type in sentiment_dict[word]:
	# 	f_out.write(word,'\t',sentiment_type,'\t',sentiment_dict[word][sentiment_type])

f_out.close()
with open('clean_port_dict.json','w') as outjson:
	json.dump(sentiment_dict, outjson)

	# for line in f_in:
	# 	word = line.split()[0]
	# 	if word not in to_remove:
	# 		print('------')
	# 		f_out.write(line)
	# f_out.close()
