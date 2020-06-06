import pandas as pd
import time 
import datetime 
from datetime import datetime, timedelta
import api 


#Pkey = 'ASDASDASD'              <<<<<< API KEYS 
#Skey = 'ASDASDASDASD '               <<<<< API KEY 
#client = Client(api_key=Pkey, api_secret=Skey)
client = api.client
 

def calc(ticker,daysdepth):
	df = pd.DataFrame(client.get_my_trades(symbol = ticker,limit=200))
	print(df)
	if not df.empty:
		df.loc[df['isBuyer'] == True, 'type'] = 'Buy'
		df.loc[df['isBuyer'] == False, 'type'] = 'Sell'
		
		df['qty'] = pd.to_numeric(df.qty)
		df['price'] = pd.to_numeric(df.price)
		df['value'] = df.price*df.qty
		
		df.loc[df['type'] == 'Buy', 'value'] = df.value*-1

		df = df[['time','symbol','type','value','price']].copy()
		
		dictionary = { "Buy": 1, "Sell": 0}
		df['id1'] = df['type'].map(dictionary)
		df['transaction'] = (df['id1']!=df['id1'].shift()).cumsum()
		
		grouped =df.groupby(['transaction'])['value'].sum()
		groupedTime =df.groupby(['transaction'])['time'].min()
		groupedPrice =df.groupby(['transaction'])['price'].max()
		
		xf = pd.DataFrame({'time':groupedTime,'price':groupedPrice,'value':grouped})

		xf.loc[xf['value'] > 0, 'type'] = 'Sell' 
		xf.loc[xf['value'] < 0, 'type'] = 'Buy'

		z = xf.loc[(xf['value'] < 0).idxmax():xf.where(xf.value > 0).last_valid_index()]


		z['time'] = pd.to_datetime(z['time'],unit='ms').copy()
		timefilter = datetime.now()-timedelta(days = daysdepth)
		z = z.where(z.time>timefilter).dropna()
		z.to_csv(f'tradeHistory_{ticker}.csv')
		print(z)
		profits = z.value.sum()
		print(profits)
		

	
		
		
	#print(df.tail(100)) 



tickers = ['BTCUSDT','BNBUSDT','XRPUSDT','ADAUSDT']
daysdepthssss = 10

for ticker in tickers: 
	calc(ticker=ticker,daysdepth=daysdepthssss)
