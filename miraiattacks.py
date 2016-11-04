#@miraiattacks parser
#modded this: http://www.craigaddyman.com/mining-all-tweets-with-python/
#thanks to @japhypoker for the regex help
#Author: @ItIsJustChad
#Last Updated: 4 Nov 2016

from twython import Twython
import time
import re
import csv

#Get your API keys from https://apps.twitter.com/ 
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN  = ''
OAUTH_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

REGEX = re.compile(r'^(.*?) - (.*?) for (\d+) seconds\s+\[Targets\]\s+(.*(?:(?!\n[Pp]ort:)\n.*)*)(?:\n[Pp]ort: (\d+))?')

CSV_FILE = open("miraiattacks.csv","wb")
TWEET_WRITER = csv.writer(CSV_FILE)

LATEST_TWEET = twitter.get_user_timeline(screen_name="miraiattacks",count=1)
LATEST_TWEET = LATEST_TWEET[0]['id']
ID_ARRAY = [LATEST_TWEET]
LAST_ID = "0"

for i in range(0, 16):
	USER_TIMELINE = twitter.get_user_timeline(screen_name="miraiattacks",
	count=200, include_retweets=False,max_id=ID_ARRAY[-1])
	for tweet in USER_TIMELINE:

        	THE_TWEET = tweet['text'].encode('utf-8')

		MATCHES = re.search(REGEX,THE_TWEET)

		if MATCHES is None:
			continue

		if not MATCHES.group(1):
			BOT = "Not found."
		else:
			BOT = MATCHES.group(1)

		if not MATCHES.group(2):
			TYPE = "Not found."
		else:
			TYPE = MATCHES.group(2)

		if not MATCHES.group(3):
			DURATION = "Not found."
		else:
			DURATION = MATCHES.group(3)

		if not MATCHES.group(4):
                        TARGETS = "Not found."
		else:
			TARGETS = MATCHES.group(4)

		if not MATCHES.group(5):
                        PORT = "Not found."
                else:
                        PORT = MATCHES.group(5)


		TWEET_WRITER.writerow((tweet['created_at'],tweet['id'],BOT,TYPE,DURATION,str(TARGETS).strip('[]'),PORT))

		print "Wrote: ", tweet['created_at'], tweet['id'], BOT, TYPE, DURATION, TARGETS, PORT

	ID_ARRAY.append(tweet['id'])
	if ID_ARRAY[len(ID_ARRAY)-2] == ID_ARRAY[len(ID_ARRAY)-1]:
		break

	time.sleep(10)

CSV_FILE.close()
