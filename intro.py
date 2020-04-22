# python : https://www.python.org/  /// HOW TO INSTALL PIP : https://pip.pypa.io/en/stable/installing/
# libraries : pandas , numpy, python-binance  
# binance wrapper docs : https://python-binance.readthedocs.io/
# VS CODE : https://code.visualstudio.com/
# FREE = Learn Basics of python:https://www.w3schools.com/python/default.asp   //https://realpython.com/ // https://www.learnpython.org/  
# PAID website but very good =   https://www.codecademy.com/catalog/language/python //  https://www.datacamp.com/
# Open acoount on binance from here and ill take commission on your trading volume everyday: https://www.binance.com/en/register?ref=27682268


import binance.client 
from binance.client import Client 
import api
import pandas as pd 
import numpy as np 

Pkey = api.Pkey
Skey = api.Skey

client = Client(api_key=Pkey, api_secret=Skey) 
tickers = ['BTCUSDT','XRPUSDT','MTLUSDT']
interval=Client.KLINE_INTERVAL_1MINUTE
depth = '1 hours ago'
def pulldata(ticker,interval,depth):
		
		Cdata = client.get_historical_klines(ticker, interval, depth)
		print(Cdata)
		df = pd.DataFrame(Cdata)
		if not df.empty: 
			
			df[0] =  pd.to_datetime(df[0],unit='ms')
			df.columns = ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
			df = df.set_index('Date')
			
			del df['IGNORE']    
			del df['BUY_VOL']
			del df['BUY_VOL_VAL']
			del df['x']

			df["Open"] = pd.to_numeric(df["Open"])
			df ["Open"] = pd.to_numeric(df["Open"])
			df ["High"] = pd.to_numeric(df["High"])
			df ["Low"] = pd.to_numeric(df["Low"])
			df ["Close"] = pd.to_numeric(df["Close"])
			df ["Volume"] = round(pd.to_numeric(df["Volume"]))
			df ["Quote_Volume"] = round(pd.to_numeric(df["Quote_Volume"]))
			df ["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
			df['div']= df['Open'] / df['Close']	

			df['Log_VolumeGain'] = (np.log(df["Quote_Volume"]/df.Quote_Volume.shift(1))*100).fillna(0)
			df['pricegain'] = (df.Open.pct_change()*100).fillna(0)

			df.to_csv(f'files/{ticker}.csv')

		print(df)

'''
for ticker in tickers: 	
	pulldata(ticker,interval,depth)
'''
x = pd.read_csv('files/MTLUSDT.csv')
print(x)

# BOT THAT CHECK DATA ON VBINANCE 
# CHECK FOR VOLUME GAINERS IN THE LAST 1 HOUR 
