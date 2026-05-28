# Install: python -m pip install -r requirements.txt --break-system-packages
# Usage: python binance-klines.py

import requests
import pandas as pd

symbol='BTCUSDT'
interval='1m'
limit=1000

params = dict(symbol=symbol, interval=interval, limit=limit)

url = 'https://api.binance.com/api/v3/klines'

resp = requests.get(url, params=params)
data = resp.json()

cols = ['open_time','open','high','low','close','volume','close_time','quote_volume','trades','taker_buy_base','taker_buy_quote','ignore']
df = pd.DataFrame(data, columns=cols)
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
numeric = ['open','high','low','close','volume','quote_volume','taker_buy_base','taker_buy_quote']
df[numeric] = df[numeric].astype(float)

print(df.head())
