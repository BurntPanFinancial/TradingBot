import time

from RecieveData import GetData, NormalizeData

namesOfStock = ["KO", "PEP"]
updateIntervalSeconds = 60


class Main:
    def __init__(self):
        self._next_update_at = time.monotonic()
        # Initial bootstrap write.
        GetData.getData(interval="5m", period="1d", namesOfStock=namesOfStock)
        NormalizeData.normalizeData(namesOfStock)

    def updateData(self):
        GetData.updateData(interval="5m", period="1d", namesOfStock=namesOfStock)
        NormalizeData.updateNormalizedData(namesOfStock)

    def performOtherActions(self):
        # Place trading logic, signal checks, etc. here.
        pass

    def run(self):
        while True:
            now = time.monotonic()
            if now >= self._next_update_at:
                print("Updating data...")
                self.updateData()
                self._next_update_at = now + updateIntervalSeconds

            self.performOtherActions()
            # Short sleep prevents busy-waiting while still allowing frequent work.
            time.sleep(0.1)


if __name__ == "__main__":
    main = Main()
    main.run()
