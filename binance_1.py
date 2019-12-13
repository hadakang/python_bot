import ccxt
import pandas as pd
import numpy as np
import json
from datetime import datetime

binance = ccxt.binance()
'''ticker = binance.fetch_ticker('ETH/BTC')
print(ticker['open'],ticker['high'],ticker['low'],ticker['close'])
'''

ohlcvs = binance.fetch_ohlcv('ETH/BTC')

'''for ohlc in ohlcvs:
    print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'))'''

print(ohlcvs)

binanceDF = pd.DataFrame(ohlcvs)

print(binanceDF)

binanceDF.columns = ["date","open","high","low","close","volume"]

print(binanceDF)

binanceDF = binanceDF.set_index('date')

print(binanceDF)

print(binanceDF.dtypes)
