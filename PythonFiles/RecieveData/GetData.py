"""Utilities for downloading and storing ticker data for backtesting."""

from pathlib import Path
from typing import Iterable

import yfinance as yf


fileNames = []


def _ticker_data_dir() -> Path:
    """Return the repo-local TickerData directory and ensure it exists."""
    data_dir = Path(__file__).resolve().parents[2] / "TickerData"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def getData(interval: str = "1h", period: str = "6mo", namesOfStock: Iterable[str] = ()) -> dict[str, str]:
    """Download OHLCV data for each ticker and save to TickerData/<ticker>_data.csv."""
    data_dir = _ticker_data_dir()
    results: dict[str, str] = {}

    for ticker in namesOfStock:
        df = yf.download(
            tickers=ticker,
            interval=interval,
            period=period,
            progress=False,
        )

        if df.empty:
            results[ticker] = "failed"
            continue

        fileNames.append([ticker, f"{interval} {period}"])
        file_name = f"{ticker}_data.csv"
        df.to_csv(data_dir / file_name)
        results[ticker] = "saved"

    return results
