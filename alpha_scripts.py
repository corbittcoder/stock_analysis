import utils
from alpha_vantage.timeseries import TimeSeries


_open = "1. open"
_high = "2. high"
_low = "3. low"
_close = "4. close"
_last_refreshed = "3. Last Refreshed"



def get_current_price(symbol, interval="1min"):
	ts = TimeSeries(key=api_key)
	data, meta = ts.get_intraday(symbol=symbol, interval=interval)	
	most_recent_time = meta[_last_refreshed]
	most_recent_close = data[most_recent_time][_close]
	return most_recent_close

#get total stock percent change for a day
def get_stock_percent_change(symbol):
	daily = get_daily_stats(symbol)
	today_close = float(daily["today"]["close"])
	yesterday_close = float(daily["yesterday"]["close"])
	return utils.get_percent_change(yesterday_close, today_close)

def get_daily_stats(symbol):
	ts = TimeSeries(key=api_key)
	data, meta = ts.get_daily(symbol=symbol)
	most_recent_time = meta[_last_refreshed]
	sorted_dates = sorted(data.keys())
	today = sorted_dates[-1]
	yesterday = sorted_dates[-2]

	todays_price = data[today]
	yesterdays_price = data[yesterday]

	return {
		"today": {
			"high": todays_price[_high],
			"low": todays_price[_low],
			"open": todays_price[_open],
			"close": todays_price[_close]
		},
		"yesterday":{
			"high": yesterdays_price[_high],
			"low": yesterdays_price[_low],
			"open": yesterdays_price[_open],
			"close": yesterdays_price[_close]
		}
	}


