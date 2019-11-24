import requests


# Binance API setup
url = "https://api.binance.com/api/v3/klines"
params = {'symbol' : 'BTCUSDT', 'interval' : '1d', 'limit' : '5'}
resp = requests.get(url, params = params)

print(resp.text)