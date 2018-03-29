import sys
sys.path.insert(0, './GetOldTweets')
import got
from textblob import TextBlob
import pandas as pd
import timeit
import re
import numpy as np

NUM_DAILY_TWEETS = 10
COMPANY = 'Amazon'

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        return analysis.sentiment.polarity

def get_day_sentiment_summary(sentiments):
    sentiment_categories = []
    for sentiment in sentiments:
        if sentiment > 0:
            sentiment_categories.append('positive')
        elif sentiment == 0:
            sentiment_categories.append('neutral')
        else:
            sentiment_categories.append('negative')
    unique, counts = np.unique(sentiment_categories, return_counts=True)
    return np.asarray((unique, counts)).T


# returns a dataframe of one column of date strings
def get_dates():
    data = pd.read_csv('data.csv')
    dates = data.iloc[:,0]
    return dates

def get_day_tweets(date):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(COMPANY).setUntil(date).setMaxTweets(NUM_DAILY_TWEETS)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)[:NUM_DAILY_TWEETS]
    return tweets

def get_twitter_sentiments(dates):
    print '\nNumber of daily tweets: ', NUM_DAILY_TWEETS, '\n'
    mean_sentiments = []
    for date in dates[0:5]:
        start = timeit.default_timer()
        print 'Day: ', date
        tweets = get_day_tweets(date)
        sentiments = []
        for tweet in tweets:
            sentiments.append(get_tweet_sentiment(tweet.text))
        mean_sentiment_value = np.mean(sentiments)
        mean_sentiments.append(mean_sentiment_value)
        print(get_day_sentiment_summary(sentiments))
        elapsed = timeit.default_timer() - start
        print 'Took this many seconds for this day\'s data: ', elapsed
        print('\n\n')
    return mean_sentiments

# returns a single column dataframe
def get_twitter_data():
    dates = get_dates()
    sentiments = get_twitter_sentiments(dates)
    df = pd.DataFrame(sentiments, dates[0:5], ['Sentiment'])
    return df

if __name__ == '__main__':
    start_time = timeit.default_timer()
    twitter_df = get_twitter_data()
    other_data_df = pd.read_csv('data.csv', index_col=0)
    combined = pd.concat([twitter_df, other_data_df], axis=1)
    combined.to_csv('all_data.csv')
    total_elapsed = timeit.default_timer() - start_time
    print 'Total number of minutes spent retrieving all data: ', total_elapsed / 60
