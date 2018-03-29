import boto3
import json
import requests
import pandas as pd
#from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from alpha_scripts import get_stock_data, get_index_moving_averages

class Stock_Analyzer():

	def __init__(self):
		#self.twitter_key = ""
		#self.google_news_key = ""
		#self.google_finance_key = ""
		pass

	def get_dates(self):
		df = get_index_moving_averages()
		dates = df.index.values
		return dates

	def get_stock_info(self, company_symbol):
		return get_stock_data(company_symbol)

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

	def save_to_csv(self, dataframe):
		dataframe.to_csv('data.csv')
