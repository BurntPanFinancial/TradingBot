"""Run data download for backtesting.

Usage examples:
    py -m pip install -r requirements.txt
    py -m PythonFiles.main
    py -m PythonFiles.main --symbols Ko PEP --interval 1h --period 6mo

Note: Yahoo Finance limits intraday intervals (<1d) to roughly the last 60 days.
For a full 6-month pull, use 1h/1d intervals instead of 5m.
"""

import argparse

from PythonFiles.RecieveData import GetData


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download ticker data into TickerData/.")
    parser.add_argument("--symbols", nargs="+", default=["Ko", "PEP"], help="Ticker symbols")
    parser.add_argument("--interval", default="1h", help="Yahoo interval (e.g. 1h, 1d)")
    parser.add_argument("--period", default="6mo", help="Yahoo period (e.g. 6mo, 1y)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        results = GetData.getData(interval=args.interval, period=args.period, namesOfStock=args.symbols)
    except ModuleNotFoundError as error:
        print(error)
        return

    for symbol, status in results.items():
        print(f"{symbol}: {status}")

    if results and all(status == "saved" for status in results.values()):
        print(f"Downloaded {args.period} of {args.interval} data for: {', '.join(args.symbols)}")
    else:
        print("One or more symbols failed to download. Check network access and symbol names.")


if __name__ == "__main__":
    main()
