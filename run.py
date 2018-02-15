from Stock_Analyzer import Stock_Analyzer


analyzer = Stock_Analyzer()

twitter_info = analyzer.get_twitter_info()
stock_info = analyzer.get_stock_info()
stock_news = analyzer.get_stock_news()
analyzer.save_to_csv()
