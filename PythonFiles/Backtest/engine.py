from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from PythonFiles.Backtest.metrics import summarize_performance
from PythonFiles.Backtest.types import Position, StrategySignal, Trade


@dataclass
class BacktestConfig:
    initial_cash: float = 10_000.0
    per_trade_fee: float = 1.0
    fill_price_column: str = "Close"


class BacktestEngine:
    """Standalone bar-by-bar simulator that runs against any strategy module."""

    def __init__(self, config: BacktestConfig):
        self.config = config

    def run(
        self,
        market_data: dict[str, pd.DataFrame],
        strategy_module: Any,
        strategy_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        strategy_params = strategy_params or {}
        cash = self.config.initial_cash
        positions = {symbol: Position() for symbol in market_data}
        trades: list[Trade] = []
        equity_rows: list[tuple[pd.Timestamp, float]] = []

        all_timestamps = sorted(
            {
                ts
                for symbol_df in market_data.values()
                for ts in symbol_df.index
            }
        )

        for timestamp in all_timestamps:
            for symbol, df in market_data.items():
                if timestamp not in df.index:
                    continue

                bar = df.loc[timestamp]
                signal = strategy_module.generate_signal(
                    symbol=symbol,
                    timestamp=timestamp,
                    data=df.loc[:timestamp],
                    position=positions[symbol],
                    params=strategy_params,
                )

                if not isinstance(signal, StrategySignal):
                    raise TypeError("Strategy must return StrategySignal")

                fill_price = float(bar[self.config.fill_price_column])
                if signal.action == "BUY" and signal.size > 0:
                    cost = fill_price * signal.size + self.config.per_trade_fee
                    if cost <= cash:
                        position = positions[symbol]
                        new_qty = position.quantity + signal.size
                        weighted_cost = (
                            position.average_price * position.quantity + fill_price * signal.size
                        )
                        position.quantity = new_qty
                        position.average_price = weighted_cost / new_qty
                        cash -= cost
                        trades.append(
                            Trade(
                                timestamp=str(timestamp),
                                symbol=symbol,
                                side="BUY",
                                quantity=signal.size,
                                price=fill_price,
                                fee=self.config.per_trade_fee,
                            )
                        )

                elif signal.action == "SELL" and signal.size > 0:
                    position = positions[symbol]
                    qty = min(signal.size, position.quantity)
                    if qty > 0:
                        proceeds = fill_price * qty - self.config.per_trade_fee
                        realized_pnl = (fill_price - position.average_price) * qty - self.config.per_trade_fee
                        position.quantity -= qty
                        if position.quantity == 0:
                            position.average_price = 0.0
                        cash += proceeds
                        trades.append(
                            Trade(
                                timestamp=str(timestamp),
                                symbol=symbol,
                                side="SELL",
                                quantity=qty,
                                price=fill_price,
                                fee=self.config.per_trade_fee,
                                pnl=realized_pnl,
                            )
                        )

            equity = cash
            for symbol, position in positions.items():
                if position.quantity <= 0:
                    continue
                df = market_data[symbol]
                if timestamp in df.index:
                    mark_price = float(df.loc[timestamp, self.config.fill_price_column])
                else:
                    mark_price = float(df[self.config.fill_price_column].iloc[-1])
                equity += position.quantity * mark_price
            equity_rows.append((timestamp, equity))

        equity_curve = pd.Series(
            [value for _, value in equity_rows],
            index=[ts for ts, _ in equity_rows],
            name="equity",
        )
        summary = summarize_performance(equity_curve)

        return {
            "summary": summary,
            "equity_curve": equity_curve,
            "trades": trades,
            "positions": positions,
            "cash": cash,
        }
