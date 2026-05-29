#!/usr/bin/env python3
"""Live Binance kline (close price) plot using WebSocket stream.

Usage:
  python scripts/live_ws_plot.py --symbol BTCUSDT --interval 1m --window 200

This script seeds recent historical klines via the REST API, then subscribes
to the WebSocket kline stream to update a live Matplotlib plot.
"""
from collections import deque
import argparse
import json
import threading
import time
import queue

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

try:
    import websocket
except Exception:
    raise SystemExit("Missing dependency 'websocket-client'. Install with: pip install websocket-client")


def fetch_historical(symbol: str, interval: str, limit: int = 200):
    url = 'https://api.binance.com/api/v3/klines'
    params = dict(symbol=symbol.upper(), interval=interval, limit=limit)
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    cols = ['open_time','open','high','low','close','volume','close_time',
            'quote_volume','trades','taker_buy_base','taker_buy_quote','ignore']
    df = pd.DataFrame(data, columns=cols)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    numeric = ['open','high','low','close','volume','quote_volume','taker_buy_base','taker_buy_quote']
    df[numeric] = df[numeric].astype(float)
    return df


class BinanceWS:
    def __init__(self, symbol: str, interval: str, out_q: queue.Queue):
        self.symbol = symbol.lower()
        self.interval = interval
        self.ws = None
        self._thread = None
        self.out_q = out_q

    def _on_message(self, wsapp, message):
        try:
            msg = json.loads(message)
            k = msg.get('k') or msg.get('data', {}).get('k')
            if not k:
                return
            item = {
                't': int(k['t']),
                'T': int(k['T']),
                'o': float(k['o']),
                'h': float(k['h']),
                'l': float(k['l']),
                'c': float(k['c']),
                'v': float(k['v']),
                'x': bool(k['x'])
            }
            # Non-blocking put
            try:
                self.out_q.put_nowait(item)
            except queue.Full:
                pass
        except Exception:
            pass

    def _on_error(self, wsapp, error):
        print('WebSocket error:', error)

    def _on_close(self, wsapp, close_status_code, close_msg):
        print('WebSocket closed')

    def _on_open(self, wsapp):
        print('WebSocket connected')

    def start(self):
        url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close,
                                         on_open=self._on_open)

        def run():
            # run_forever blocks; run it in a daemon thread
            self.ws.run_forever(ping_interval=20, ping_timeout=10)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self):
        try:
            if self.ws:
                self.ws.close()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--interval', default='1m')
    parser.add_argument('--window', type=int, default=200, help='Number of points to display')
    parser.add_argument('--refresh', type=int, default=1000, help='Plot refresh interval in ms')
    args = parser.parse_args()

    q = queue.Queue(maxsize=1000)

    print('Seeding historical data...')
    df = fetch_historical(args.symbol, args.interval, limit=args.window)
    # deque of dicts
    window = deque(maxlen=args.window)
    for _, row in df.iterrows():
        window.append({'t': int(row['open_time'].timestamp() * 1000), 'c': float(row['close'])})

    ws = BinanceWS(args.symbol, args.interval, q)
    ws.start()

    try:
        plt.style.use('seaborn-darkgrid')
    except Exception:
        # Fallbacks if seaborn-specific style isn't available in this environment
        try:
            plt.style.use('seaborn')
        except Exception:
            plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 5))
    line, = ax.plot([], [], '-o', markersize=3)

    def fmt_ts(ms_ts):
        return datetime.fromtimestamp(ms_ts / 1000.0)

    def update_plot(frame):
        # drain queue
        updated = False
        while True:
            try:
                item = q.get_nowait()
                # use close price and timestamp
                # if same timestamp as last, replace
                if window and item['t'] == window[-1]['t']:
                    window[-1] = {'t': item['t'], 'c': item['c']}
                else:
                    window.append({'t': item['t'], 'c': item['c']})
                updated = True
            except queue.Empty:
                break

        if not updated and not window:
            return line,

        times = [fmt_ts(d['t']) for d in window]
        closes = [d['c'] for d in window]
        ax.clear()
        ax.plot(times, closes, '-o', markersize=3)
        ax.set_title(f"{args.symbol.upper()} {args.interval} — Live close price")
        ax.set_ylabel('Price')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        fig.autofmt_xdate()
        return line,

    import matplotlib.animation as animation
    ani = animation.FuncAnimation(fig, update_plot, interval=args.refresh)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        ws.stop()


if __name__ == '__main__':
    main()
