
import binance.client 
from binance.client import Client 
import api
import pandas as pd 
import numpy as np 

#Pkey = 'ASDASDASD'              <<<<<< API KEYS 
#Skey = 'ASDASDASDASD '               <<<<< API KEY 
#client = Client(api_key=Pkey, api_secret=Skey)
client = api.client


def pullData(ticker,interval,depth):
	raw = client.get_historical_klines(ticker, interval, depth)
	raw = pd.DataFrame(raw)
	print(raw)
	if not raw.empty:
						raw[0] =  pd.to_datetime(raw[0],unit='ms')
						print(raw)
						raw.columns = ['timestamp','open','high','low','close','volume','IGNORE','quoteVolume','SELLVolume','BUY_VOL','BUY_VOL_VAL','x']
						
						del raw['IGNORE']    
						del raw['BUY_VOL']
						del raw['BUY_VOL_VAL']
						del raw['x']
						del raw['SELLVolume']


						# convert to numbers 
						raw ["open"] = pd.to_numeric(raw["open"])
						raw ["high"] = pd.to_numeric(raw["high"])
						raw ["low"] = pd.to_numeric(raw["low"])
						raw ["close"] = pd.to_numeric(raw["close"])
						raw ["volume"] = round(pd.to_numeric(raw["volume"]))
						raw ["quoteVolume"] = round(pd.to_numeric(raw["quoteVolume"]))
						raw.loc[raw.quoteVolume < 100, 'quoteVolume'] =100

						raw['pchange1h'] = raw.close.diff(1).fillna(0) # diff can has if for different timeperiods 
						raw['pchange1hpct'] = round((raw['pchange1h']/raw ["close"])*100,2)

						raw['pchange24h'] = raw.close.diff(23).fillna(0) # diff can has if for different timeperiods 
						raw['pchange24hpct'] = round((raw['pchange24h']/raw ["close"])*100,2)

						raw['v1h'] = raw.quoteVolume.rolling(window = 1).sum().fillna(0)#.shift()

						raw['vchange1h'] = raw.v1h.diff(1).fillna(0) # diff can has if for different timeperiods 
						raw['vchange1hpct'] = round((raw['vchange1h']/raw ["quoteVolume"])*100,2)
					
						raw['v4h'] = raw.quoteVolume.rolling(window = 4).sum().fillna(0)#.shift()
						raw['vchange4h'] = raw.v4h.diff(4).fillna(0) # diff can has if for different timeperiods 
						raw['vchange4hpct'] = round((raw['vchange4h']/raw ["quoteVolume"])*100,2)
						
						raw['v24'] = raw.quoteVolume.rolling(window = 23).sum().fillna(0)#.shift()
						raw['vchange24h'] = raw.v24.diff(23).fillna(0) # diff can has if for different timeperiods 
						raw['vchange24hpct'] = round((raw['vchange24h']/raw ["quoteVolume"])*100,2)

						print(raw)

						return raw 
					
		



					










