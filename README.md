# TradingBot

## Download data for backtesting

From repo root:

```bash
py -m pip install -r requirements.txt
py -m PythonFiles.main --symbols Ko PEP --interval 1h --period 6mo
```

Notes:
- `5m` data is not available for a full 6 months on Yahoo Finance; use `1h` or `1d`.
- CSV files are saved to `TickerData/<SYMBOL>_data.csv`.
