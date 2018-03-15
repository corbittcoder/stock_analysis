import boto3
import json
import requests
import pandas as pd
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

class Stock_Analyzer():

	def __init__(self):
		#self.twitter_key = ""
		#self.google_news_key = ""
		#self.google_finance_key = ""
		pass


	def get_twitter_info(self):
		ACCESS_TOKEN = ''
		ACCESS_SECRET = ''
		CONSUMER_KEY = ''
		CONSUMER_SECRET = ''

		oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

		# Initiate the connection to Twitter Streaming API
		twitter_stream = TwitterStream(auth=oauth)

		# Get a sample of the public data following through Twitter
		iterator = twitter_stream.statuses.sample()

		# Print each tweet in the stream to the screen
		# Here we set it to stop after getting 1000 tweets.
		# You don't have to set it to stop, but can continue running
		# the Twitter API to collect data for days or even longer.
		tweet_count = 1000
		for tweet in iterator:
			tweet_count -= 1
			# Twitter Python Tool wraps the data returned by Twitter
			# as a TwitterDictResponse object.
			# We convert it back to the JSON format to print/score
			print(json.dumps(tweet))

			# The command below will do pretty printing for JSON data, try it out
			# print json.dumps(tweet, indent=4)

			if tweet_count <= 0:
				break

	def get_stock_info(self):
		api_key = 'ZXKLYB9LPX4Q4RXN'
		symbol = 'MSFT'

		url = ("https://www.alphavantage.co/query?"
			   "function=TIME_SERIES_DAILY&"
			   "symbol=" + symbol +
			   "&apikey=" + api_key)

		response = requests.get(url)
		dictionary = response.json()



	def get_stock_news(self):
		api_key = ''

		# select date
		date = '2018-02-05'
		# select company name
		KeyWord = 'Microsoft'

		url = ('https://newsapi.org/v2/everything?'
				'q=' + KeyWord + '&'
				'from=' + date + '&'
				'sortBy=popularity&'
				'apiKey=' + api_key)

		response = requests.get(url)

		# creates a python dictionary
		dictionary = response.json()
		print(type(dictionary))

		# look through all popular articles that day and print the title and description
		for i in range(len(dictionary['articles'])):
			print(dictionary['articles'][i]['title'])
			print(dictionary['articles'][i]['description'])


	# Takes string to test sentiment
	# Returns {
	# 	"Positive|Negative|Mixed|Neutral": "Number between 0-1"
	# }
	def get_sentiment_analysis(self, string):
		session = boto3.Session(profile_name='stock_sentiment')
		comprehend = session.client(service_name='comprehend', region_name='us-west-2')
		sentiment_response = comprehend.detect_sentiment(Text = string, LanguageCode="en")
		sentiment = sentiment_response["Sentiment"]

		# Get highest score from response
		sentiment = sentiment[0] + sentiment[1:].lower()
		sentiment_score = {sentiment: sentiment_response["SentimentScore"][sentiment]}
		return sentiment_score

	def save_to_csv(self):
		pass #implement
