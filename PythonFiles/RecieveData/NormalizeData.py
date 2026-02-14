# from this import s
# wtf is this import from chat?????
tickers = []


def normalizeData(tickers=[]):
    if not tickers:
        print("No tickers provided")
        return
    # Normalize data for each ticker
    for ticker in tickers:
        # Normalize data for each ticker
        # create a new file for each ticker and normalize it
        file = open(f"../TickerData/{ticker}_data.csv", "r")
        skipLines = 3
        for _ in range(skipLines):
            next(file)
        normalizedFile = open(f"../TickerData/{ticker}_normalized.csv", "w")

        for line in file:
            line = line.strip().split(",")
            point1 = float(line[4])
            point2 = float(line[1])
            percentChange = normalizeDataPoints(point1, point2)
            # print(f"{ticker}: {percentChange:.2f}%")
            normalizedFile.write(f"{percentChange:.2f}%\n")
        normalizedFile.close()
        file.close()
        print("")


def updateNormalizedData(tickers=[]):
    if not tickers:
        print("No tickers provided")
        return
    for ticker in tickers:
        dataPath = f"../TickerData/{ticker}_data.csv"
        normalizedPath = f"../TickerData/{ticker}_normalized.csv"

        with open(dataPath, "r") as file:
            skipLines = 3
            for _ in range(skipLines):
                next(file)
            latestLine = None
            for line in file:
                latestLine = line.strip()

            normalizedFile = open(normalizedPath, "w")
            if latestLine is None:
                print(f"No data found for {ticker}")
                continue

            point1 = float(latestLine.split(",")[4])
            point2 = float(latestLine.split(",")[1])
            percentChange = normalizeDataPoints(point1, point2)
            normalizedFile.write(f"{percentChange:.2f}%\n")

            print(f"added {percentChange} to {normalizedPath}\n")
        normalizedFile.close()
        file.close()
        print("")


def normalizeDataPoints(point1, point2):
    # Calculate the percent change between two points
    percentChange = ((point2 - point1) / point1) * 100
    return percentChange
