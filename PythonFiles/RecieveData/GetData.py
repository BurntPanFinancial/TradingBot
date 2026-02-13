# will be run in a virtual environment
import os

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
        # assume that the file already exists and we are updating it

        fileName_buff = f"{fileNames[i][0]}_data_buffer.csv"
        fileName = f"{fileNames[i][0]}_data.csv"

        df.to_csv(f"../TickerData/{fileName_buff}")
        buff = open(f"../TickerData/{fileName_buff}", "r")
        lineCount = 0
        for line in buff:
            lineCount += 1

        # reset the buffer file position
        buff.seek(0)
        for line in range(lineCount - 1):
            buff.readline()

        mainFile = open(f"../TickerData/{fileName}", "a")
        # this is the last line in the buffer file, which would be the most recent
        appendLine = buff.readline()
        mainFile.write(appendLine)
        buff.close()
        mainFile.close()
        print(f"added {appendLine} to {fileName}\n")
        os.remove(f"../TickerData/{fileName_buff}")
        # df.to_csv(f"../TickerData/{fileName}", mode="a", header=False)
        # add the latest row from the buffer file to the main file
        # this doesn't work because we are looking at the top, but appending would add to the bottom
        # f = open(f"../TickerData/{fileName}")
        # line = f.readline()
