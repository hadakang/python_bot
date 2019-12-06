import requests
import pandas as pd
from pandas import DataFrame as df
import datetime
import numpy as np

# Binance API setup
url = "https://api.binance.com/api/v3/klines"
params = {'symbol' : 'BTCUSDT', 'interval' : '1d', 'limit' : '365'}
resp = requests.get(url, params = params)


# json to DataFrame / Column selection & rename / datetime adjust
content1 = pd.read_json(resp.text) # resp.json()
df = pd.DataFrame(content1)
df = df[[0, 1, 2, 3, 4, 5]]
df = df.rename(columns = {0 : 'datetime', 
                          1 : 'open', 
                          2 : 'high', 
                          3 : 'low', 
                          4 : 'close', 
                          5 : 'volume'})
# df = df.astype(float)
df['datetime'] = df['datetime'].astype('datetime64[ms]')


# MDD 계산하기
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)


# 현재 수수료는 예제 기준
fee = 0.0032
df['ror'] = np.where(df['high'] > df['target'],
                    df['close'] / df['target'] - fee,
                    1)

df['hpr'] = df['ror'].cumprod() # cumprod 도대체 뭐가 문제지...?
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])