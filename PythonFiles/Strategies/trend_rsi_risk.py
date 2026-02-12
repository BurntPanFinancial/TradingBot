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
    """Trend + RSI strategy with volatility and risk controls.

    Logic:
    - Enter long only when trend is up (fast EMA > slow EMA), RSI is not overbought,
      and current volatility is below a configurable threshold.
    - Exit long on trend breakdown, overbought reversal, hard stop-loss, or trailing stop.
    """

    fast_ema = int(params.get("fast_ema", 20))
    slow_ema = int(params.get("slow_ema", 100))
    rsi_window = int(params.get("rsi_window", 14))
    entry_rsi_max = float(params.get("entry_rsi_max", 62.0))
    exit_rsi_min = float(params.get("exit_rsi_min", 45.0))
    stop_loss_pct = float(params.get("stop_loss_pct", 0.03))
    trailing_stop_pct = float(params.get("trailing_stop_pct", 0.04))
    max_volatility = float(params.get("max_volatility", 0.03))
    order_size = int(params.get("order_size", 1))

    min_bars = max(slow_ema, rsi_window) + 2
    if len(data) < min_bars:
        return StrategySignal(action="HOLD", reason="warming_up")

    close = data["Close"].astype(float)

    ema_fast = close.ewm(span=fast_ema, adjust=False).mean().iloc[-1]
    ema_slow = close.ewm(span=slow_ema, adjust=False).mean().iloc[-1]

    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.rolling(window=rsi_window).mean().iloc[-1]
    avg_loss = loss.rolling(window=rsi_window).mean().iloc[-1]
    if avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

    returns = close.pct_change().dropna()
    volatility = returns.rolling(window=rsi_window).std().iloc[-1]
    if pd.isna(volatility):
        volatility = 0.0

    latest_price = close.iloc[-1]

    if position.quantity > 0:
        stop_price = position.average_price * (1.0 - stop_loss_pct)
        trailing_reference = close.tail(min(40, len(close))).max()
        trailing_stop = trailing_reference * (1.0 - trailing_stop_pct)

        if latest_price <= stop_price:
            return StrategySignal(action="SELL", size=position.quantity, reason=f"{symbol} stop_loss")

        if latest_price <= trailing_stop:
            return StrategySignal(action="SELL", size=position.quantity, reason=f"{symbol} trailing_stop")

        if ema_fast < ema_slow or rsi < exit_rsi_min:
            return StrategySignal(action="SELL", size=position.quantity, reason=f"{symbol} trend_or_momentum_exit")

        return StrategySignal(action="HOLD", reason=f"{symbol} keep_position")

    trend_up = ema_fast > ema_slow
    momentum_ok = rsi <= entry_rsi_max
    volatility_ok = volatility <= max_volatility

    if trend_up and momentum_ok and volatility_ok:
        return StrategySignal(action="BUY", size=order_size, reason=f"{symbol} trend_momentum_entry")

    return StrategySignal(action="HOLD", reason=f"{symbol} no_entry")
