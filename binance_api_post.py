import hmac
import hashlib
import requests
import json
import time
from urllib.parse import urljoin, urlencode

API_KEY = 'teNJpK1KE4Ob0AjPbXyRv32mkKeMZDQsXsloxahDA4UQVKsG9Br6YEReuTJmFc2y'
SECRET_KEY = '4DOgqDeSZe4UEFAIVAxDoX5aJNeP11DEFVAg8Oc2KmUmh3drSfMd2kNos04FIujt'
headers = {
    'X-MBX-APIKEY' : API_KEY
}
BASE_URL = 'https://api.binance.com'
PATH = '/api/v3/order/test'
timestamp = int(time.time() * 1000)

params = {
    'symbol' : 'BTCUSDT',
    'side' : 'BUY',
    'type' : 'LIMIT',
    'timeInForce' : 'GTC',
    'quantity' : 1,
    'price' : 3000,
    'timestamp' : timestamp
}

query_string = urlencode(params)
params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

url = urljoin(BASE_URL, PATH)
r = requests.post(url, headers = headers, params = params)

data = r.json()
print(json.dumps(data, indent = 2))