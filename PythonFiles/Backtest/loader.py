from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_ticker_csv(csv_path: Path) -> pd.DataFrame:
    """
    Load a Yahoo Finance intraday CSV exported by this repository.

    The source files currently include a 3-row header. This function normalizes
    that format into a standard OHLCV dataframe indexed by UTC timestamp.
    """

    df = pd.read_csv(csv_path, skiprows=3)
    if df.empty:
        raise ValueError(f"No rows found in {csv_path}")

    df.columns = ["Datetime", "Close", "High", "Low", "Open", "Volume"]
    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
    df = df.set_index("Datetime").sort_index()
    return df


def load_market_data(data_dir: Path, symbols: list[str]) -> dict[str, pd.DataFrame]:
    """Load and normalize market data for every symbol in the backtest run."""

    market_data: dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        csv_name = f"{symbol}_data.csv"
        csv_path = data_dir / csv_name
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing data file: {csv_path}")
        market_data[symbol] = load_ticker_csv(csv_path)
    return market_data
