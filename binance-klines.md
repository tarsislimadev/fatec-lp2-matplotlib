# Binance Klines (Candlesticks) — Quick Reference

This file explains the Binance Spot API "klines" (candlestick) endpoint and the corresponding WebSocket stream. See the official docs: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints

## What is a Kline

A kline (candlestick) is a summary of trading activity over a fixed time interval. Each kline includes open/high/low/close prices, volumes, and time boundaries.

## REST Endpoint

GET /api/v3/klines

Query parameters:
- `symbol` (required): trading pair, e.g. `BTCUSDT`.
- `interval` (required): kline interval, e.g. `1m`, `5m`, `1h`, `1d`.
- `startTime` (optional): start time in milliseconds.
- `endTime` (optional): end time in milliseconds.
- `limit` (optional): number of results, default 500, max 1000.

Example request:

```
GET https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100
```

## Response Format (REST)

Response is an array of arrays (each sub-array is one kline). Fields (by index):

0. Open time (ms)
1. Open price (string)
2. High price (string)
3. Low price (string)
4. Close price (string)
5. Volume (string) — base asset volume
6. Close time (ms)
7. Quote asset volume (string)
8. Number of trades (int)
9. Taker buy base asset volume (string)
10. Taker buy quote asset volume (string)
11. Ignore (string) — historical leftover field

Example single kline (formatted):

```json
[1622505600000, "35000.00", "35100.00", "34950.00", "35050.00", "12.345", 1622505659999, "432000.00", 123, "6.789", "238000.00", "0"]
```

Interpretation: open at 35000.00 at timestamp 1622505600000, closed at 35050.00, volume 12.345 BTC, etc.

## Intervals

Common interval values:
- `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`.

## Python REST Example

```python
import requests
import pandas as pd
from datetime import datetime

url = 'https://api.binance.com/api/v3/klines'
params = dict(symbol='BTCUSDT', interval='1m', limit=200)
resp = requests.get(url, params=params)
data = resp.json()

# Convert to DataFrame with readable columns
cols = ['open_time','open','high','low','close','volume','close_time',
        'quote_volume','trades','taker_buy_base','taker_buy_quote','ignore']
df = pd.DataFrame(data, columns=cols)
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
numeric = ['open','high','low','close','volume','quote_volume','taker_buy_base','taker_buy_quote']
df[numeric] = df[numeric].astype(float)
print(df.head())
```

## WebSocket Kline Stream

URL: `wss://stream.binance.com:9443/ws/{symbol_lower}@kline_{interval}`

Example: `wss://stream.binance.com:9443/ws/btcusdt@kline_1m`

Message structure (JSON) delivers an event with a `k` object (kline):

Key fields in `k` object:
- `t`: kline start time (ms)
- `T`: kline close time (ms)
- `s`: symbol
- `i`: interval
- `f`:`L`: first and last trade IDs
- `o`,`h`,`l`,`c`: open/high/low/close prices
- `v`: base asset volume
- `n`: number of trades
- `x`: boolean, whether this kline is final (closed) or still updating
- `q`: quote asset volume
- `V`: taker buy base asset volume
- `Q`: taker buy quote asset volume

Example (abridged):

```json
{
  "e": "kline",
  "E": 123456789,
  "s": "BTCUSDT",
  "k": {
    "t": 1622505600000,
    "T": 1622505659999,
    "s": "BTCUSDT",
    "i": "1m",
    "f": 100,
    "L": 200,
    "o": "35000.00",
    "c": "35050.00",
    "h": "35100.00",
    "l": "34950.00",
    "v": "12.345",
    "n": 123,
    "x": false,
    "q": "432000.00",
    "V": "6.789",
    "Q": "238000.00",
    "B": "0"
  }
}
```

Note: `x=true` indicates the kline is closed/final — you can persist it. While `x=false`, the kline is updating in real time.

## Tips and Best Practices
- Use `limit` and `startTime`/`endTime` to page through historical data reliably.
- For long ranges, request in chunks (max 1000 per call) and respect rate limits.
- On the WebSocket, buffer incomplete (x=false) kline updates in memory and only write finalized (x=true) klines to persistent storage.
- Convert timestamps (ms) to timezone-aware datetimes in your application.
- Beware of symbol casing: REST API expects uppercase `BTCUSDT`; WebSocket stream uses lowercase in the URL path.

## Where to Learn More
- REST docs: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- WebSocket docs: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams

---

This file is a compact reference for fetching and interpreting Binance kline (candlestick) data.
