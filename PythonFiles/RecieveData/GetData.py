# will be run in a virtual environment
import yfinance as yf

# storing name of file + intervalPeriod for each file
fileNames = []


def getData(interval="5m", period="1d", namesOfStock=[]):
    # namesOfStock = ["MSFT", "AAPL", "NVDA"]
    # namesOfStock = ["K0", "PEP"]

    # interval = "1h"
    # period = "2d"

    for i in range(len(namesOfStock)):
        df = yf.download(
            tickers=namesOfStock[i], interval=interval, period=period, progress=False
        )
        fileNames.append([namesOfStock[i], interval + " " + period])
        # print(fileNames[i])
        fileName = f"{fileNames[i][0]}_data.csv"
        df.to_csv(f"../TickerData/{fileName}")


def updateData(interval="5m", period="5m", namesOfStock=[]):
    for i in range(len(namesOfStock)):
        df = yf.download(
            tickers=namesOfStock[i], interval=interval, period=period, progress=False
        )
        fileNames.append([namesOfStock[i], interval + " " + period])
        # print(fileNames[i])
        fileName = f"{fileNames[i][0]}_data.csv"
        # assume that the file already exists and we are updating it
        df.to_csv(f"../TickerData/{fileName}", mode="a", header=False)


# add interval names to the end of fileNames
# intervalPeriod = interval + " " + period
# fileNames.append(intervalPeriod)
