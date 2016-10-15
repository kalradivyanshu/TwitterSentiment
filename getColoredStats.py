import urllib.request
import json
import cv2
import numpy as np
from bs4 import BeautifulSoup
from random import randint
import math
import operator
import time
from textblob import TextBlob
import tweepy

#"xycfufwfpcovwavj"


# Step 1 - Authenticate
consumer_key= 'CONSUMER_KEY_HERE'
consumer_secret= 'CONSUMER_SECRET_HERE'

access_token='ACCESS_TOKEN_HERE'
access_token_secret='ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def getSentiment(api, key):
	public_tweets = api.search(key)
	AvgSentiment = 0
	noOfTweets = len(public_tweets)
	sum1 = 0
	for tweet in public_tweets:
		text = tweet.text
		cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '#' and 'http' not in word and word != 'RT'])
		#print(cleanedtext)
		analysis = TextBlob(cleanedtext)
		sentiment = analysis.sentiment.polarity
		sum1 += sentiment

		if sentiment == 0:
			#ignore since not a opinion, its a general statement
			noOfTweets -= 1
	if noOfTweets > 0:
		AvgSentiment = sum1/noOfTweets
	return AvgSentiment

def getxy(coordinates,raduis):
	x2 = 0
	y2 = 0
	while True:
		x2 = randint(2*radius,width-radius)
		y2 = randint(2*radius,height-radius)
		flag = 0
		for key, value in coordinates.items():
			x1 = int(key.split()[0])
			y1 = int(key.split()[1])
			ans = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
			if ans < value + radius+50:
				flag = 1
				break
		if flag == 0:
			break
	return x2, y2

def drawOnImage(img, radius, AvgSentiment, key):
	img = cv2.circle(img,(x,y), radius, (0, 127.5+(AvgSentiment*127.5), 127.5+(AvgSentiment*-127.5)), -1)
	font = cv2.FONT_HERSHEY_PLAIN
	string = key
	#coordinates.append(str(x)+" "+str(y)+" "+key)
	cv2.putText(img,string,(x-8*len(string)-5,y), font, 2,(255,255,255),2,cv2.LINE_AA)
	string = str(value)+'+'
	cv2.putText(img,string,(x-8*len(string)-5,y+40), font, 2,(255,255,255),2,cv2.LINE_AA)
	return img

url=urllib.request.urlopen("http://www.google.com/trends/hottrends/atom/feed").read().decode("utf-8")

soup=BeautifulSoup(url, features="xml")
title = []
for element in soup.find_all('title'):
	#print(element.string)
	if element.string == "Hot Trends":
		continue
	title.append(element.string)

views = []
for element in soup.find_all('approx_traffic'):
	view = element.string.replace(',','')
	view = view.strip('+')
	views.append(int(view))

i = 0
trends = dict()
for element in title:
	trends[element] = views[i]
	i += 1

height = 2280
width = 3120
img = np.zeros((height,width,3), np.uint8)

sum = 0
for view in views:
	sum = sum + view
trends = sorted(trends.items(), key=operator.itemgetter(1))
trends = dict(trends)
coordinates = dict()
flag = 0
for key, value in trends.items():
	radius = int(float(value)/float(sum)*250+100)

	AvgSentiment = getSentiment(api, key)
	print(key, AvgSentiment)
	
	if flag == 0:
		x = randint(2*radius,width-radius)
		y = randint(2*radius,height-radius)
		coordinates[str(x)+" "+str(y)] = radius
		flag = 1
	elif flag == 1:
		x,y = getxy(coordinates, radius)
		coordinates[str(x)+" "+str(y)] = radius

	img = drawOnImage(img, radius, AvgSentiment, key)

imgname = "./"+str(time.strftime("%d%m%Y"))+".png"
print(imgname)
cv2.imwrite(imgname,img)