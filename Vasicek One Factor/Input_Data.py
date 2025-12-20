import pandas as pd
import numpy as np
import datetime as dt

def main():
    curve_historical_data = pd.read_excel('SOFR.xlsx')
    curve_historical_data['Effective Date'] = pd.to_datetime(curve_historical_data['Effective Date'])
    curve_historical_data = curve_historical_data[curve_historical_data['Effective Date'] <= '2025-01-02']
    rates = curve_historical_data['Rate (%)']/100
    print(curve_historical_data.head())
    return rates

if __name__ == "__main__":
    main()
