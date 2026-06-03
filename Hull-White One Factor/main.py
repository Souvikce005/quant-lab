from data_loader import DataLoader
from curves import Curve

class main:

    def __init__(self):
        pass    

    rates_data = DataLoader.load(r"/Users/souvikchakraborty/IR-Modelling/Data/synthetic_rates.xlsx")

    print(rates_data)
    