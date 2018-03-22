import utils
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
