import pandas as pd 
import time 
import datetime 
from datetime import datetime, timedelta
import api 

#Pkey = 'ASDASDASD'              <<<<<< API KEYS 
#Skey = 'ASDASDASDASD '               <<<<< API KEY 
#client = Client(api_key=Pkey, api_secret=Skey)

client = api.client


def PLCalculator(ticker,account,client,depthInDays):
		startdate = datetime.now()-timedelta(days=depthInDays)
		df = pd.DataFrame(client.get_my_trades(symbol = ticker,limit=1000))
		
		if not df.empty:
			df.loc[df['isBuyer'] == True, 'type'] = 'Buy' 
			df.loc[df['isBuyer'] == False, 'type'] = 'Sell'
			df['qty'] = pd.to_numeric(df.qty)
			df['price'] = pd.to_numeric(df.price)
			df['value'] = df.price*df.qty
			df.loc[df['type'] == 'Buy', 'value'] = df.value*-1
			df = df[['time','symbol','type','value','price']]

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
			#print(xf,z)
			#z['time'] = pd.to_datetime(z['time'],unit='ms')
			
			tradesLog = pd.DataFrame()

			for i,j in z.iterrows():
				if j.type =='Buy':
						buyPrice = j.price 
						buyTime = j.time
						buyValue = j.value

						df =z.where(z.time>buyTime).dropna()
						for i,x in df.iterrows():
							if x.type =='Sell':
								sellPrice = x.price
								sellTime = x.time 
								sellValue =x.value
								
								tradesLog = tradesLog.append(pd.DataFrame({'ticker':ticker,'buyTime':buyTime,'buyPrice':buyPrice,'buyValue':buyValue,'sellTime':sellTime,'sellPrice':sellPrice,'sellValue':sellValue}, index = [0]))
								break
			
			if not tradesLog.empty:
				tradesLog['buyTime']	=  pd.to_datetime(tradesLog['buyTime'],unit='ms')	
				tradesLog['sellTime']	=pd.to_datetime(tradesLog['sellTime'],unit='ms')	
				tradesLog = tradesLog.where(tradesLog.buyTime>startdate).dropna()	
				tradesLog['PL'] = pd.to_numeric(tradesLog.buyValue)+pd.to_numeric(tradesLog.sellValue)
				
				sumTicker = pd.DataFrame()
				PL = tradesLog['PL'].sum()
				sumTicker = sumTicker.append(pd.DataFrame({'ticker':ticker,'profitLoss':PL}, index = [0]))
	
				sumTicker.to_csv(f'tradesLog/tradeslogSUM{account}{depthInDays}.csv',index=False,mode='a')
				tradesLog.to_csv(f'tradesLog/tradeslogRAW{account}.csv',index=False,mode='a',header=False)
				print(tradesLog)

tickers = ['NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT', 'PAXUSDT', 'USDCUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'USDSUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'GTOUSDT', 'ERDUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'NPXSUSDT', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'MCOUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'EURUSDT', 'OGNUSDT', 'DREPUSDT', 'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'STRATUSDT', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT', 'XZCUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'BTCUPUSDT', 'BTCDOWNUSDT', 'GXSUSDT', 'ARDRUSDT', 'LENDUSDT', 'MDTUSDT']
account = 'yt_testing'
depthInDays = 2

df = pd.DataFrame()
#RESET FILES FROM PERV PULL
df.to_csv(f'tradesLog/tradeslogSUM{account}{depthInDays}.csv')
df.to_csv(f'tradesLog/tradeslogRAW{account}{depthInDays}.csv')

for ticker in tickers: 
		try:
					PLCalculator(ticker,account,client,depthInDays)
					df = pd.read_csv(f'tradesLog/tradeslogSUM{account}{depthInDays}.csv')	
					df = df.drop_duplicates()
					df.to_csv(f'tradesLog/tradeslogSUM{account}{depthInDays}.csv',index=False)						
					print(df)
		except:
			pass

