import tweepy
from textblob import TextBlob
import sys
import csv

if len(sys.argv) >= 2:
	topic = sys.argv[1]
else:
	print("By default topic is Trump.")
	topic = "Trump"

consumer_key= 'CONSUMER_KEY_HERE'
consumer_secret= 'CONSUMER_SECRET_HERE'

access_token='ACCESS_TOKEN_HERE'
access_token_secret='ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('Trump')

with open('sentiment.csv', 'w', newline='\n') as  f:

	writer = csv.DictWriter(f, fieldnames=['Tweet', 'Sentiment'])
	writer.writeheader()
	for tweet in public_tweets:
		text = tweet.text
		#Cleaning tweet
		cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] == '.' and word[0] != '#' and 'http' not in word and word != 'RT'])
		
		analysis = TextBlob(cleanedtext)

		sentiment = analysis.sentiment.polarity
		if sentiment >= 0:
			polarity = 'Positive'
		else:
			polarity = 'Negative'

		#print(cleanedtext, polarity)

		writer.writerow({'Tweet':text, 'Sentiment':polarity})
