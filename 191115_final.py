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
dataDF = dataDF.append({"date":"","open":"0.0","high":"0.0","low":"0.0","close":"0.0","volume":"0.0"},ignore_index = True)

num =len(upbitData2)

print (num)

for i in range (0,num):
    dataDF.loc[i,"date"] = upbitData2[i]['candle_date_time_utc']
    dataDF.loc[i,"open"] = float(upbitData2[i]['opening_price'])
    dataDF.loc[i,"high"] = float(upbitData2[i]['high_price'])
    dataDF.loc[i,"low"] = float(upbitData2[i]['low_price'])
    dataDF.loc[i,"close"]= float(upbitData2[i]['prev_closing_price'])
    dataDF.loc[i,"volume"]= float(upbitData2[i]['candle_acc_trade_volume'])

print(dataDF.dtypes)

#데이터 타입 변경
dataDF2 = dataDF.astype({'open':float,'high':float,'low':float,'close':float,'volume':float})

#데이터 타입 확인
print(dataDF2.dtypes)

#MA계산
#closeData = dataDF2['close']
#ma5 = closeData.rolling(5).mean()
#print(ma5)

dataDF2 = dataDF2.set_index('date')

print(dataDF2)
'''
dataDF2['range'] = (dataDF2['high']-dataDF2['low'])*0.5
#dataDF['rangeshift1'] = dataDF['range'].shift(1)
dataDF2['target'] = dataDF2['open'] + dataDF2['range'].shift(1)

print(dataDF2)


print(dataDF2)

dataDF2['ror'] = np.where(dataDF2['high']>dataDF2['target'],dataDF2['close']/dataDF2['target'],1)

ror2 = dataDF2['ror'].cumprod()[-2]

print(ror2)


'''

'''
#변동성 돌파 백테스팅 

def get_ror(k=0.5):
    dataDF2['range'] = (dataDF2['high']-dataDF2['low'])*k
    dataDF2['target'] = dataDF2['open'] + dataDF2['range'].shift(1)
    fee = 0.0032
    dataDF2['ror'] = np.where(dataDF2['high']>dataDF2['target'],dataDF2['close']/dataDF2['target']-fee,1)

    ror = dataDF2['ror'].cumprod()[-2]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror =get_ror(k)
    print("%.1f %f" % (k,ror))

'''
## 변동성 돌파 & 상승장 전략 백테스팅

dataDF2['ma5'] = dataDF2['close'].rolling(window=5).mean().shift(1)
dataDF2['range'] = (dataDF2['high'] - dataDF2['low']) * 0.5
dataDF2['target'] = dataDF2['open'] + dataDF2['range'].shift(1)
dataDF2['bull'] = dataDF2['open'] > dataDF2['ma5']

fee = 0.0032

dataDF2['ror'] = np.where((dataDF2['high'] > dataDF2['target']) & dataDF2['bull'],dataDF2['close'] / dataDF2['target'] - fee,1)

dataDF2['hpr'] = dataDF2['ror'].cumprod()
dataDF2['dd'] = (dataDF2['hpr'].cummax()-dataDF2['hpr']) / dataDF2['hpr'].cummax()*100

print("MDD: ",dataDF2['dd'].max())
print("HPR: ",dataDF2['hpr'][-2])