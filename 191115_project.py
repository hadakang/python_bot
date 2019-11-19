import datetime
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import ssl
import urllib.request
import json
import pandas as pd

with urllib.request.urlopen("https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=100") as upbitApiUrl:
    upbitData = upbitApiUrl.read().decode('utf8')
 #   soup = BeautifulSoup(data,"html5lib")

print(upbitData)
#print(soup)

upbitData2 = json.loads(upbitData)

print (upbitData2)

dataDF = pd.DataFrame()
dataDF = dataDF.append({"date":"","open":"","high":"","low":"","close":"","volume":""},ignore_index = True)

print (dataDF)

num =len(upbitData2)

print (num)

print (upbitData2[0]['market'])

for i in range (0,num):
    dataDF.ix[i,"date"] = upbitData2[i]['candle_date_time_utc']
    dataDF.ix[i,"open"] = upbitData2[i]['opening_price']
    dataDF.ix[i,"high"] = upbitData2[i]['high_price']
    dataDF.ix[i,"low"] = upbitData2[i]['low_price']
    dataDF.ix[i,"close"]=upbitData2[i]['prev_closing_price']
    dataDF.ix[i,"volume"]=upbitData2[i]['candle_acc_trade_volume']

print(dataDF)
#upbitUrl = urllib.urlopen(upbitApiUrl)
#upbitUrlData = json.load(upbitApiUrl.read())

#upbitUrlDataDF = pd.DataFrame()
#upbitUrlDataDF = upbitUrlDataDF.append({"opening_price":"","high_price":"","low_price":""},ignore_index=True)

#upbitUrlDataDF

