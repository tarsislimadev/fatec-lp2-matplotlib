# Project Fatec: Binance klines on Matplotlib

A small demo that fetches Binance kline (candlestick) data and visualizes it with Matplotlib. It includes a live plot that seeds recent history via the REST API and then subscribes to Binance's WebSocket kline stream for real-time updates.

## Quick start (guests)

0. Clone the repository

```bash
git clone https://github.com/tarsislimadev/fatec-lp2-matplotlib.git
```

2. Install Python 3.10+ (or use your existing Python environment).
3. Install required packages:

```bash
python -m pip install -r requirements.txt
```

3. Start the live plot (example):

```bash
python scripts/live_ws_plot.py --symbol BTCUSDT --interval 1m --window 200
```

What the command does:
- Seeds the plot with the last `--window` historical klines for `--symbol`.
- Subscribes to Binance's WebSocket `kline` stream and updates the plot in real time.

Common options:
- `--symbol` (default: `BTCUSDT`) — trading pair to display
- `--interval` (default: `1m`) — kline interval
- `--window` (default: `200`) — number of historical points to seed and show
- `--refresh` (default: `1000`) — plot refresh interval in ms

## Troubleshooting
- If you see an error about `seaborn-darkgrid` not found, install `seaborn` or adjust the script's style fallback.
- If `websocket-client` is missing, run `python -m pip install websocket-client`.
- The script prints `WebSocket connected` then `WebSocket closed` when the plot window is closed or the connection drops; network interruptions can also close the socket.

## Next steps and contributions
- Add candlestick (OHLC) rendering instead of close-only lines.
- Persist finalized kline data (`x==true`) to CSV or a local database.
- Implement automatic reconnect with exponential backoff.

If you want any of the above, open an issue or submit a PR.

## Static plot (historical)

To fetch historical klines and save a static close-price plot:

```bash
python scripts/historical_plot.py --symbol BTCUSDT --interval 1m --limit 200 --output figures/btcusdt_1m.png
```

The generated image will be saved under `figures/`.

## Files

- [scripts/live_ws_plot.py](scripts/live_ws_plot.py) — live WebSocket plot (real-time updates)
- [scripts/historical_plot.py](scripts/historical_plot.py) — fetch historical klines and save PNG
- [requirements.txt](requirements.txt) — Python dependencies

## Setup (optional)

It's recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows PowerShell
python -m pip install -r requirements.txt
```

## References

Binance REST & WebSocket docs:
- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams

## License

[MIT](./LICENSE)
