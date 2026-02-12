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

## Run backtests

SMA crossover baseline:

```bash
python -m PythonFiles.backtest_main \
  --symbols Ko PEP \
  --strategy PythonFiles.Strategies.sma_crossover \
  --initial-cash 10000 \
  --fee 1.0 \
  --fast-window 5 \
  --slow-window 20 \
  --order-size 1
```

Trend + RSI + risk-managed strategy:

```bash
python -m PythonFiles.backtest_main \
  --symbols Ko PEP \
  --strategy PythonFiles.Strategies.trend_rsi_risk \
  --initial-cash 10000 \
  --fee 1.0 \
  --order-size 1 \
  --strategy-param fast_ema=20 \
  --strategy-param slow_ema=100 \
  --strategy-param rsi_window=14 \
  --strategy-param entry_rsi_max=62 \
  --strategy-param exit_rsi_min=45 \
  --strategy-param stop_loss_pct=0.03 \
  --strategy-param trailing_stop_pct=0.04 \
  --strategy-param max_volatility=0.03
```
