import pandas as pd 
from binance.client import Client 

import VG_Clean


def VolumeGainers(ticker,interval,depth):
  df = VG_Clean.pullData(ticker,interval,depth)
  def updatSymbolInfo(df,ticker,interval):
      print(df)
      #PRICE  
      
      lastprice = (list(df.close.tail(1)))[0] #lastprice
      
      pchange1hpct = (list(df.pchange1hpct.tail(1)))[0] #Pchange1H_pct

      pchange24hpct = (list(df.pchange24hpct.tail(1)))[0] #Pchange24H_pct

    
      #VOLUME 
      vchange1h = (list(df.vchange1h.tail(1)))[0] #Vchange1H
      vchange1hpct = (list(df.vchange1hpct.tail(1)))[0] #vchange1hpct

      vchange4h = (list(df.vchange4h.tail(1)))[0] #Vchange4H
      vchange4hpct = (list(df.vchange4hpct.tail(1)))[0] #Vchange4H


      vchange24h = (list(df.vchange24h.tail(1)))[0] #vchange24h
      vchange24hpct = (list(df.vchange24hpct.tail(1)))[0] #Vchange24H_pct
      
      volume24h = (list(df.v24.tail(1)))[0] #vchange24h

      # to return the total values and then ditribute data on the dicts
      return lastprice,pchange1hpct,pchange24hpct,vchange1h,vchange1hpct,vchange4h,vchange4hpct,volume24h,vchange24h,vchange24hpct

  lastprice,pchange1hpct,pchange24hpct,vchange1h,vchange1hpct,vchange4h,vchange4hpct,volume24h,vchange24h,vchange24hpct = updatSymbolInfo(df,ticker,interval)
  print(lastprice,pchange1hpct,pchange24hpct,vchange1h,vchange1hpct,vchange4h,vchange4hpct,volume24h,vchange24h,vchange24hpct)  
    #if BTC 

  x = pd.DataFrame()
  x = x.append(pd.DataFrame({'symbol':ticker,
      'interval':interval,
      'lastPrice':lastprice,
      'volume_24h':volume24h,
      'priceChangePercent_1h':pchange1hpct,
      'priceChangePercent_24h':pchange24hpct,
      'volumeChange_1h':vchange1h,
      'volumeChangePercent_1h':vchange1hpct,
      'volumeChange_4h':vchange4h,
      'volumeChangePercent_4h':vchange4hpct,
      'volumeChange_24h':vchange24h,
      'volumeChangePercent_24h':vchange24hpct},index = [0]))
  x.to_csv('VolumeGainers.csv',index= False, mode = 'a',header =False)


tickers = ['BTCUSDT','ETHUSDT','BNBUSDT','NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT', 'PAXUSDT', 'USDCUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'USDSUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'GTOUSDT', 'ERDUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'NPXSUSDT', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'MCOUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'EURUSDT', 'OGNUSDT', 'DREPUSDT', 'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'STRATUSDT', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT', 'XZCUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'BTCUPUSDT', 'BTCDOWNUSDT', 'GXSUSDT', 'ARDRUSDT', 'LENDUSDT', 'MDTUSDT']
interval = Client.KLINE_INTERVAL_1HOUR
depth = '40 hours ago'

'''
for ticker in tickers: 
  VolumeGainers(ticker,interval,depth)
'''


df = pd.read_csv('VolumeGainers.csv')
df = df.sort_values(by=['volumeChange_4h','priceChangePercent_1h'],ascending=['False','False'])
x = df[['symbol','volumeChange_4h','volumeChange_24h','priceChangePercent_1h']].copy()
print(x.tail(20))

#volumeChange_1h