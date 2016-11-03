#@miraiattacks parser
#modded this: http://www.craigaddyman.com/mining-all-tweets-with-python/
#Author: ItsJustChad
#Last updated: 11/2/2016

from twython import Twython
import time
import re
import csv

#get keys from apps.twitter.com
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN  = ''
OAUTH_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

BOT_REGEX = re.compile(r'.*?-\s')
TYPE_REGEX = re.compile(r'-\s.*flood')
DURATION_REGEX = re.compile(r'\d+\Wseconds')
TARGET_REGEX = re.compile(r'\d+\.\d+\.\d+\.\d+\/\d+')
PORT_REGEX = re.compile(r'[P|p]ort:\s+\d+')

CSV_FILE = open("miraiattacks.csv","wb")
TWEET_WRITER = csv.writer(CSV_FILE)

LATEST_TWEET = twitter.get_user_timeline(screen_name="miraiattacks",count=1)
LATEST_TWEET = LATEST_TWEET[0]['id']
ID_ARRAY = [LATEST_TWEET]

for i in range(0, 16):
	USER_TIMELINE = twitter.get_user_timeline(screen_name="miraiattacks",
	count=200, include_retweets=False,max_id=ID_ARRAY[-1])
	for tweet in USER_TIMELINE:
        	THE_TWEET = tweet['text'].encode('utf-8')
		BOT = re.findall(BOT_REGEX,THE_TWEET)
		if not BOT:
			BOT = "None"
		else:
			BOT = BOT[0][:len(BOT[0])-3]

		TYPE = re.findall(TYPE_REGEX,THE_TWEET)
		if not TYPE:
			TYPE = "None"
		else:
			TYPE = TYPE[0][2:]

		DURATION = re.findall(DURATION_REGEX,THE_TWEET)
		if not DURATION:
			DURATION = "None"
		else:
			DURATION = DURATION[0]

		TARGETS = re.findall(TARGET_REGEX,THE_TWEET)
		if not TARGETS:
			TARGETS = "None"

		PORT = re.findall(PORT_REGEX,THE_TWEET)
		if not PORT:
			PORT = "None"
		else: 
			PORT = PORT[0][6:]

		TWEET_WRITER.writerow((tweet['created_at'],tweet['id'],BOT,TYPE,DURATION,TARGETS,PORT))

		print "Wrote: ", tweet['created_at'], tweet['id'], BOT, TYPE, DURATION, TARGETS, PORT

	ID_ARRAY.append(tweet['id'])
	if ID_ARRAY[len(ID_ARRAY)-1] == ID_ARRAY[len(ID_ARRAY)-2]:
		break
	else:
		time.sleep(10)

CSV_FILE.close()
