import requests
import pandas as pd
from pandas import DataFrame as df
import numpy as np

# upbit api request (multiple request necessary when data exceed 200 limit)
url = "https://api.upbit.com/v1/candles/days"
querystring_1 = {"market" : "KRW-BTC" , "count" : "200"}
response_1 = requests.request("GET", url, params = querystring_1)
querystring_2 = {"market" : "KRW-BTC" , "to":"2018-05-01 00:00:00", "count" : "164"}
response_2 = requests.request("GET", url, params = querystring_2)

# concatenating multiple requests
data1 = pd.read_json(response_1.text)
data2 = pd.read_json(response_2.text)
data = pd.concat([data1, data2])

# data parsing & column rename & sort index
df = pd.DataFrame(data, columns = ['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume'])
df = df.set_index('candle_date_time_kst')
df = df.rename(columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                                "candle_acc_trade_volume": "volume"})
df = df.sort_index()

# backtest

'''
# find max k value
def get_ror(k=0.5):
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    # 현재 수수료는 예제 기준 추후 upbit 기준 계산해서 수정하기
    fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'],
                        df['close'] / df['target'] - fee,
                        1)

    ror = df['ror'].cumprod()[-2]
    return(ror)


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k,ror))
### max ror이 나오는 k 값을 자동으로 출력해줄 수는 없을까?
'''


# MDD 계산하기
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

# 현재 수수료는 예제 기준 추후 upbit 기준 계산해서 수정하기
fee = 0.0032
df['ror'] = np.where(df['high'] > df['target'],
                    df['close'] / df['target'] - fee,
                    1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
