import requests
import pandas as pd
from pandas import DataFrame as df
import datetime


### Calculate target price based on yesterday's ohlc
url = "https://api.binance.com/api/v3/klines"
params = {'symbol' : 'BTCUSDT', 'interval' : '1d', 'limit' : '2'}
resp = requests.get(url, params = params)
# print(resp.text)

content = pd.read_json(resp.text)
df = pd.DataFrame(content)
df = df[[0, 1, 2, 3, 4]]
df = df.rename(columns = {0 : 'datetime', 
                          1 : 'open', 
                          2 : 'high', 
                          3 : 'low', 
                          4 : 'close'})
df['datetime'] = df['datetime'].astype('datetime64[ms]')
yesterday = df.iloc[0]
## 개선점 -> yesterday 변수에 담을 필요 없이 바로 각 변수로 할당
# print(yesterday) 

open = yesterday[1]
high = yesterday[2]
low = yesterday[3]
close = yesterday[4]
# print([open, high, low, close])

## maybe need to add round up later
range = (high - low) * 0.5
target = open + range
# print([range, target])


import hmac
import hashlib
import json
import time
from urllib.parse import urljoin, urlencode


API_KEY = 'teNJpK1KE4Ob0AjPbXyRv32mkKeMZDQsXsloxahDA4UQVKsG9Br6YEReuTJmFc2y'
SECRET_KEY = '4DOgqDeSZe4UEFAIVAxDoX5aJNeP11DEFVAg8Oc2KmUmh3drSfMd2kNos04FIujt'
headers = {
    'X-MBX-APIKEY' : API_KEY
}
BASE_URL = 'https://api.binance.com'
timestamp = int(time.time() * 1000)


### Check account order 
PATH_OPEN = '/api/v3/openOrders'

params_open = {
    'symbol' : 'BTCUSDT',
    'timestamp' : timestamp
}

query_string_open = urlencode(params_open)
params_open['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string_open.encode('utf-8'), hashlib.sha256).hexdigest()

url_open = urljoin(BASE_URL, PATH_OPEN)
r_open = requests.get(url_open, headers = headers, params = params_open)

## parse r_open to extract open order & cancel order

### Check account balance
PATH_ACCOUNT = '/api/v3/account'

params_acct = {'timestamp' : timestamp}

query_string_acct = urlencode(params_acct)
params_acct['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string_acct.encode('utf-8'), hashlib.sha256).hexdigest()

url_acct = urljoin(BASE_URL, PATH_ACCOUNT)
r_acct = requests.post(url_acct, headers = headers, params = params_acct)

# print(r_acct.text)
## 개선점 -> btc_amt 변수에 현재 가지고 있는 BTC 개수 담기


### Sell last day's order (market sell)

PATH_SELL = '/api/v3/order/'

params_sell = {
    'symbol' : 'BTCUSDT',
    'side' : 'SELL',
    'type' : 'MARKET',
    'quantity' : btc_amt,
    'timestamp' : timestamp
}


### Put in order based on target price
PATH_ORDER = '/api/v3/order/'
timestamp = int(time.time() * 1000)

params = {
    'symbol' : 'BTCUSDT',
    'side' : 'BUY',
    'type' : 'LIMIT',
    'timeInForce' : 'GTC',
    'quantity' : 1,
    'price' : target,
    'timestamp' : timestamp
}

## need to find a way to calculate quantity

query_string = urlencode(params)
params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

url = urljoin(BASE_URL, PATH)
r = requests.post(url, headers = headers, params = params)

# data = r.json()
print(r.text)