#!/usr/bin/env python3
"""Fetch historical klines from Binance REST API and create a static plot.

Usage:
  python scripts/historical_plot.py --symbol BTCUSDT --interval 1m --limit 500 --output figures/btcusdt_1m.png

The script saves the figure and (optionally) shows it.
"""
import argparse
import os
from datetime import datetime

import requests
import pandas as pd
import matplotlib.pyplot as plt


def fetch_klines(symbol: str, interval: str, limit: int = 500):
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


def plot_close(df: pd.DataFrame, symbol: str, interval: str, output: str, show: bool = False):
    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
    try:
        plt.style.use('seaborn')
    except Exception:
        try:
            plt.style.use('seaborn-darkgrid')
        except Exception:
            plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['open_time'], df['close'], '-', linewidth=1)
    ax.set_title(f"{symbol.upper()} {interval} — Close price")
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output, dpi=300)
    print(f"Saved plot to {output}")
    if show:
        plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--interval', default='1m')
    parser.add_argument('--limit', type=int, default=500)
    parser.add_argument('--output', default='figures/klines.png')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    print('Fetching historical klines...')
    df = fetch_klines(args.symbol, args.interval, limit=args.limit)
    plot_close(df, args.symbol, args.interval, args.output, show=args.show)


if __name__ == '__main__':
    main()
