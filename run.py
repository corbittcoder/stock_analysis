from Stock_Analyzer import Stock_Analyzer

company = 'AMZN'
analyzer = Stock_Analyzer()

#print(analyzer.get_sentiment_analysis("Hello, today is a great day"))
#twitter_info = analyzer.get_twitter_info()
stock_info = analyzer.get_stock_info(company)
#stock_news = analyzer.get_stock_news()
analyzer.save_to_csv(stock_info)
