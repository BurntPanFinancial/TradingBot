"""
Standalone backtest runner.

Usage:
1) Download historical data first (existing pipeline writes `TickerData/<SYMBOL>_data.csv`).
2) Run from repo root:
   python -m PythonFiles.backtest_main \
       --symbols KO PEP \
       --strategy PythonFiles.Strategies.sma_crossover \
       --initial-cash 10000 \
       --fee 1.0

To plug in a new strategy module, implement a `generate_signal(...)` function
that returns `PythonFiles.Backtest.types.StrategySignal`.
"""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from PythonFiles.Backtest.engine import BacktestConfig, BacktestEngine
from PythonFiles.Backtest.loader import load_market_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run standalone backtests using pluggable strategies")
    parser.add_argument("--symbols", nargs="+", required=True, help="Ticker symbols matching CSV names")
    parser.add_argument("--strategy", required=True, help="Python module path for the strategy")
    parser.add_argument("--data-dir", default="TickerData", help="Directory containing <SYMBOL>_data.csv files")
    parser.add_argument("--initial-cash", type=float, default=10_000.0)
    parser.add_argument("--fee", type=float, default=1.0)
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    parser.add_argument("--order-size", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    strategy_module = importlib.import_module(args.strategy)

    market_data = load_market_data(Path(args.data_dir), args.symbols)

    engine = BacktestEngine(
        BacktestConfig(
            initial_cash=args.initial_cash,
            per_trade_fee=args.fee,
        )
    )

    result = engine.run(
        market_data=market_data,
        strategy_module=strategy_module,
        strategy_params={
            "fast_window": args.fast_window,
            "slow_window": args.slow_window,
            "order_size": args.order_size,
        },
    )

    print("Backtest summary")
    for key, value in result["summary"].items():
        print(f"- {key}: {value}")
    print(f"- trades: {len(result['trades'])}")


if __name__ == "__main__":
    main()
