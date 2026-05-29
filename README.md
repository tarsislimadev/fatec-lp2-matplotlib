# Project Fatec: Binance klines on MatPlotLib

A small demo that fetches Binance kline (candlestick) data and visualizes it with Matplotlib. It includes a live plot that seeds recent history via the REST API and then subscribes to Binance's WebSocket kline stream for real-time updates.

## Quick start (guests)

1. Install Python 3.10+ (or use your existing Python environment).
2. Install required packages:

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

## References

Binance REST & WebSocket docs:
- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams

## License

[MIT](./LICENSE)
