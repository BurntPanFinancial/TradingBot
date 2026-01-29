# Press the green button in the gutter to run the script.
from PythonFiles.RecieveData import GetData
namesOfStock = ["Ko", "PEP"]

class Main:
    def __init__(self):
        GetData.getData(interval ="5m", period ="1d", namesOfStock = namesOfStock)
        # everything should be saves as files for the first time around

Main()