import requests
import pandas as pd
from pandas import DataFrame as df
import pyupbit
#from pandas import DataFrame

# Upbit API sample
url = "https://api.upbit.com/v1/candles/days"
querystring_1 = {"market" : "KRW-BTC" , "count" : "200"}
response_1 = requests.request("GET", url, params = querystring_1)

# 추가 캔들 165개 요청
querystring_2 = {"market" : "KRW-BTC" , "to":"2018-05-01 00:00:00", "count" : "164"}
response_2 = requests.request("GET", url, params = querystring_2)


# pandas의 read_json 통해서 데이터 가져오기 & 2개 데이터프레임 합치기
data1 = pd.read_json(response_1.text)
data2 = pd.read_json(response_2.text)
data = pd.concat([data1, data2])

# print(data)
# KEY 확인 // print(data.keys())

# kst 기준 날짜를 index로 지정 & 필요 column만 가져오기 & column 이름 변경
df = pd.DataFrame(data, columns = ['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume'])
df = df.set_index('candle_date_time_kst')
df = df.rename(columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                                "candle_acc_trade_volume": "volume"})

# index 오름차순으로 재정렬
df = df.sort_index()
print(df.head())
print(df.tail())



'''
# candle_date_time_kst 인덱스 지정
df_index = df['candle_date_time_kst']
print(df_index)
'''

'''
# JSON method 통해서 가져오기 
data = response.json()
df = DataFrame(data)
print(df)
'''
''' 
# read json 통해서 변환
data = pd.read_json(response.text)
print(data)
'''

'''
data = response.text
df = DataFrame(data)

print(df)
'''