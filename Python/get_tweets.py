from pymongo import MongoClient

from pprint import pprint
from tqdm import tqdm
import calendar,csv
from config import ES_URI, MG_URI

mgclient = MongoClient(MG_URI)
from config import ES_URI, MG_URI
from lib_time import datetime_from_timestamp, datetime_from_str
from lib_time import datetime_to_timestamp, datetime_to_str, get_time_elapsed
from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')


DATABASE = 'inep'


# timestamp_now = int(time())
# datetime_now = datetime_from_timestamp(timestamp_now, utc=True)
# datetime_now = datetime_to_str(datetime_now, '%d-%m-%Y')
# datetime_now = datetime_from_str(datetime_now, '%d-%m-%Y')
# timestamp_now = datetime_to_timestamp(datetime_now)

# # get finish timestamp
# timestamp_end = timestamp_now - (7*3600*24)
# datetime_end = datetime_from_timestamp(timestamp_end, utc=True)
# datetime_end = datetime_to_str(datetime_end, '%d-%m-%Y')
# datetime_end = datetime_from_str(datetime_end, '%d-%m-%Y')
# timestamp_end = datetime_to_timestamp(datetime_end)

# convert to miliseconds
# time_zone = 7200*1000
# # time_ajust = 3600*24*3
# time_ajust = 0
# timestamp_now = (timestamp_now * 1000) -time_ajust
# timestamp_end = (timestamp_end * 1000) -time_ajust

# set to query tweets from now

db = mgclient[DATABASE]
col = db['tweets']

timestamp_query_fixo = calendar.timegm(datetime.strptime('11-11-2017 15:00','%d-%m-%Y %H:%M').utctimetuple())*1000

queryStart = {'status.timestamp_ms': {"$gte": timestamp_query_fixo}}
queryEnd = {'status.timestamp_ms': {"$lte": timestamp_query_fixo+(24*3600*1000)}}
query_not_retweet = {'status.retweeted_status':{'$exists':False}}

query = {"$and":[queryStart,queryEnd,query_not_retweet]}
col_find = col.find(query).limit(1000)
print(col.find(query).count())
with open('tweets_enem.csv','w') as out_file:

	spamwriter = csv.writer(out_file, delimiter=',',quotechar='"')
	for data in col_find:
		text = []
		text.append(data['status']['text'])
		spamwriter.writerow(text)




quit()

# for i in range(1,72):

# 	time_fixing = (i-1)*3600*1000
# 	timestamp_query = timestamp_query_fixo+ time_fixing

# 	queryStart = {'status.timestamp_ms': {"$gte": timestamp_query}}
#     queryEnd = {'status.timestamp_ms': {"$lte": timestamp_query+(3600*1000)}}
#     query_not_retweet = {'status.retweeted_status':{'$exists':false}}
#     query = {"$and":[queryStart,queryEnd,query_not_retweet]}
#     col_find = col.find(query)
#     col_total = col.find(query)
#     if(col_total>100)
# 	for data in tqdm(col_find[0:200], total=200):
# 		text = data['status']['text']


