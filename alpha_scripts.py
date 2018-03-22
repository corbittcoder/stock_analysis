import utils
import json
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

def get_sma(symbol):
	ti = TechIndicators(key='GU7Q0FX7R704IRRZ', output_format='pandas')
	all_data, meta = ti.get_sma(symbol, interval='daily', series_type='close')
	return all_data.tail(1261)[:-1]

def get_ema(symbol):
	ti = TechIndicators(key='GU7Q0FX7R704IRRZ', output_format='pandas')
	all_data, meta = ti.get_ema(symbol, interval='daily', series_type='close')
	return all_data.tail(1261)[:-1]

def get_company_daily_price(symbol):
	ts = TimeSeries(key='GU7Q0FX7R704IRRZ')
	company_all_data, company_meta = ts.get_daily(symbol=symbol, outputsize='full')
	index_all_data, index_data = ts.get_daily(symbol='IVV', outputsize='full')
	keys_company = sorted(company_all_data.keys())[-1261:]
	keys_index = sorted(index_all_data.keys())[-1261:]
	differences = []
	dates = []
	for i in range(len(keys_company)-1):
		company_previous_day_close = float(company_all_data[keys_company[i]][_close])
		company_next_day_close = float(company_all_data[keys_company[i+1]][_close])

		index_previous_day_close = float(index_all_data[keys_company[i]][_close])
		index_next_day_close = float(index_all_data[keys_company[i+1]][_close])

		company_percent_change = utils.get_percent_change(company_previous_day_close, company_next_day_close)
		index_percent_change = utils.get_percent_change(index_previous_day_close, index_next_day_close)
		
		diff = company_percent_change - index_percent_change
		differences.append(diff)
	data = { 
		'dates': keys_company[:-1],
		'percent_difference': differences
	}
	data_df = pd.DataFrame(data)
	data_df = data_df.set_index('dates')
	return data_df

def get_comp_moving_averages(company_symbol):
	sma_df = get_sma(company_symbol)
	ema_df = get_ema(company_symbol)
	combined = pd.concat([ema_df, sma_df], axis=1)
	return combined

def get_index_moving_averages():
	df = get_comp_moving_averages('IVV')
	df = df.rename({'SMA': 'Index_SMA', 'EMA': 'Index_EMA'}, axis='columns')
	return df

def get_moving_averages(company_symbol):
	comp_df = get_comp_moving_averages(company_symbol)
	index_df = get_index_moving_averages()
	combined = pd.concat([comp_df, index_df], axis=1)
	return combined
