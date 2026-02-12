from __future__ import annotations

import pandas as pd

from PythonFiles.Backtest.types import Position, StrategySignal


def generate_signal(
    symbol: str,
    timestamp,
    data: pd.DataFrame,
    position: Position,
    params: dict,
) -> StrategySignal:
    """Simple example strategy module used by the standalone backtester."""

    fast_window = int(params.get("fast_window", 5))
    slow_window = int(params.get("slow_window", 20))
    order_size = int(params.get("order_size", 1))

    if len(data) < slow_window:
        return StrategySignal(action="HOLD")

    fast_sma = data["Close"].rolling(window=fast_window).mean().iloc[-1]
    slow_sma = data["Close"].rolling(window=slow_window).mean().iloc[-1]

    if fast_sma > slow_sma and position.quantity == 0:
        return StrategySignal(action="BUY", size=order_size, reason=f"{symbol} bullish crossover")

    if fast_sma < slow_sma and position.quantity > 0:
        return StrategySignal(action="SELL", size=position.quantity, reason=f"{symbol} bearish crossover")

    return StrategySignal(action="HOLD")
