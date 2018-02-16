import requests

api_key = ''

#select date
date = '2018-02-05'
#select company name
KeyWord = 'Microsoft'

url = ('https://newsapi.org/v2/everything?'
       'q=' +KeyWord +'&'
       'from='+ date+'&'
       'sortBy=popularity&'
       'apiKey=' + api_key)

response = requests.get(url)

#creates a python dictionary
dictionary = response.json()

#look through all popular articles that day and print the title and description
for i in range(len(dictionary['articles'])):
    print(dictionary['articles'][i]['title'])
    print(dictionary['articles'][i]['description'])
