import requests
import json
import time
import pandas as pd
from Stock_Analyzer import Stock_Analyzer
import boto3
from datetime import datetime

def get_company_news(start=20130323, end=20180323):
	ny_times_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
	payload =  {
		'api-key': "",
		'fq': 'headline:("Amazon")ORsnippet:("Amazon")',
		'begin_date': "20130323",
		'end_date': "20180323",
		'sort': "oldest",
		'fl': "web_url,snippet,headline,pub_date",
		'page': 0
	}
	response = requests.get(ny_times_url, params=payload).json()
	hits = response['response']['meta']['hits']
	pages = (hits / 10) + 1
	articles = [response]
	for page in range(1, pages):
		time.sleep(1)
		payload['page'] = page
		response = requests.get(ny_times_url, params=payload).json()
		articles.append(response)
		
	print(json.dumps(articles, indent=4))

def get_news_sentiment():
	analyzer = Stock_Analyzer()	
	with open('ny_times.json', 'r') as ny_fd:
		articles = json.load(ny_fd)

	date_to_sentiment = {}
	for page in articles:
		docs = page['response']['docs']
		for article in docs:
			pub_date = article['pub_date']
			snippet = article['snippet']
			if not snippet:
				snippet = article['headline']['main']
			sentiment = analyzer.get_sentiment_analysis(snippet)
			value = 0
			if sentiment.keys()[0].lower() == 'positive':
				value = 1
			elif sentiment.keys()[0].lower() == 'negative':
				value = -1
			
			date_to_sentiment[pub_date] = value
	with open('output.json', 'w') as o_fd:
		o_fd.write(json.dumps(date_to_sentiment, indent=4))
	#pub_date = datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%SZ')	

def analyze_sentiments():
	with open('output.json', 'r') as o_fd:
		date_to_sentiment = json.load(o_fd)
	formatted_dates = {}
	data = {
		'dates': [],
		'news_sentiment': []
	}
	for key, value in sorted(date_to_sentiment.items()):
		try:
			date_formatted = datetime.strptime(key, '%Y-%m-%dT%H:%M:%SZ')	
		except ValueError:
			date_formatted = datetime.strptime(key, '%Y-%m-%dT%H:%M:%S+0000')	
		date_formatted = date_formatted.strftime("%Y-%m-%d")
		formatted_dates[date_formatted] = value
		data['dates'].append(date_formatted)
		data['news_sentiment'].append(value)
		
	with open('output2.json', 'w') as o2_fd:
		o2_fd.write(json.dumps(formatted_dates, indent=4))

	data_df = pd.DataFrame(data)
	data_df = data_df.set_index('dates')
	print(data_df.head(100))
	return data_df

#get_company_news()
#get_news_sentiment()
analyze_sentiments()
