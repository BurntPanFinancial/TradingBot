from __future__ import annotations

import pandas as pd


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    """Return max drawdown as a decimal (e.g. -0.18 for -18%)."""

    running_peak = equity_curve.cummax()
    drawdown = (equity_curve - running_peak) / running_peak
    return float(drawdown.min())


def summarize_performance(equity_curve: pd.Series) -> dict[str, float]:
    """Build a compact performance summary for the completed backtest run."""

    start = float(equity_curve.iloc[0])
    end = float(equity_curve.iloc[-1])
    total_return = (end - start) / start
    max_drawdown = calculate_max_drawdown(equity_curve)
    return {
        "start_equity": start,
        "end_equity": end,
        "total_return": total_return,
        "max_drawdown": max_drawdown,
    }
