import pandas as pd
import numpy as np
import datetime as dt

def main():
    curve_historical_data = pd.read_excel(r'/Users/souvikchakraborty/IR-Modelling/Vasicek One Factor/SOFR.xlsx')
    curve_historical_data['Effective Date'] = pd.to_datetime(curve_historical_data['Effective Date'])
    curve_historical_data['Rates'] = curve_historical_data['Rate (%)']/100
    return curve_historical_data

if __name__ == "__main__":
    main()
