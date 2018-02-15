import boto3
import json
import requests
import pandas as pd

class Stock_Analyzer():

	def __init__(self):
		self.twitter_key = ""
		self.google_news_key = ""
		self.google_finance_key = ""

	def get_twitter_info(self):
		pass

	def get_stock_info(self):
		pass

	def get_stock_news(self):
		pass


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
		pass
