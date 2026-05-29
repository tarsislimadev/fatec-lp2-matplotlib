# Project Fatec: Binance klines on MatPlotLib

## Running the live plot

Requirements are listed in `requirements.txt`. Install them with:

```bash
python -m pip install -r requirements.txt
```

Run the live WebSocket plot to view real-time close prices (example):

```bash
python scripts/live_ws_plot.py --symbol BTCUSDT --interval 1m --window 200
```

Options:
- `--symbol`: trading pair (default: `BTCUSDT`)
- `--interval`: kline interval (default: `1m`)
- `--window`: number of historical points to seed and display (default: `200`)
- `--refresh`: plot refresh interval in milliseconds (default: `1000`)

Notes:
- The script seeds historical data via the REST API then subscribes to Binance's WebSocket kline stream.
- Install `websocket-client` if missing.

## References

https://github.com/orlandosaraivajr/FATEC_1SEM26_LP2/issues/6

https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-api-information

https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints

## License

[MIT](./LICENSE)
