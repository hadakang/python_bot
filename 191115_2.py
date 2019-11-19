import datetime
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import ssl
import urllib.request
import json
import pandas as pd
import numpy as np
import pyupbit

with urllib.request.urlopen("https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=100") as upbitApiUrl:
    upbitData = upbitApiUrl.read().decode('utf8')

upbitData2 = json.loads(upbitData)

dataDF = pd.DataFrame()
dataDF = dataDF.append({"date":"","open":"","high":"","low":"","close":"","volume":""},ignore_index = True)

num =len(upbitData2)

print (num)

for i in range (0,num):
    dataDF.loc[i,"date"] = upbitData2[i]['candle_date_time_utc']
    dataDF.loc[i,"open"] = upbitData2[i]['opening_price']
    dataDF.loc[i,"high"] = upbitData2[i]['high_price']
    dataDF.loc[i,"low"] = upbitData2[i]['low_price']
    dataDF.loc[i,"close"]=upbitData2[i]['prev_closing_price']
    dataDF.loc[i,"volume"]=upbitData2[i]['candle_acc_trade_volume']

print(dataDF)

closeData = dataDF['close']
ma5 = closeData.rolling(5).mean()
print(ma5)

dataDF['range'] = (dataDF['high']-dataDF['low'])*0.5
#dataDF['rangeshift1'] = dataDF['range'].shift(1)
dataDF['target'] = dataDF['open'] + dataDF['range'].shift(1)

print(dataDF)

dataDF['ror'] = np.where(dataDF['high']>dataDF['target'],dataDF['close']/dataDF['target'],1)

#dataDF.to_excel("trace.xlsx")

#ror = dataDF['ror']

#print(ror)

#ror2 = dataDF['ror'].cumprod()[-2]

#print(ror2)

#print(dataDF)

def get_ror(k=5):
    dataDF['range'] = (dataDF['high']-dataDF['low'])*k
    dataDF['target'] = dataDF['open'] + dataDF['range'].shift(1)
    fee = 0.0032
    dataDF['ror'] = np.where(dataDF['high']>dataDF['target'],dataDF['close']/dataDF['target']-fee,1)

    ror = dataDF['ror'].cumprod()[-2]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror =get_ror(k)
    print("%.1f %f" % (k,ror))



