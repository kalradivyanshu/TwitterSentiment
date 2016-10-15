# TwitterSentiment

# CSV Generator
The CSVGenerate takes recent tweets on the given topic and generates a CSV with 2 columns, Tweet and Sentiment ('Positive/Negative').

Usage:

``` python3 CSVGenerate.py topic ```

# Get Colored Stats

The get colored stats gets the google trending topics of the day and then searches twitter for tweets on the topics. Then it creates an image consisting of circles for each topic, the larger the circle the more it was googled. And the color of the circle indicates the general opinion of twitter users in that topic. The more red the color the more negative tweets it has had, and green color means more postive tweets (it calculates average sentiment for each topic).

Dependencies:

tweepy
textblob
OpenCV
BeautifulSoup
Numpy

Usage:

``` python3 getColoredStats.py ```

Output (15th Oct 2016) :

![alt tag](https://raw.githubusercontent.com/kalradivyanshu/TwitterSentiment/master/15102016.png)
