import pandas as pd
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import Input_Data
import Simulator
import logging

logging.basicConfig(level=logging.INFO)

def read_SOFR_data():
    rates_data = pd.read_excel('SOFR.xlsx')
    rates_data['Effective Date'] = pd.to_datetime(rates_data['Effective Date'])
    rates_data = rates_data[(rates_data['Effective Date'] > '2025-01-02') & (rates_data['Effective Date'] <= '2025-02-03')]
    actual_rates = rates_data['Rate (%)']/100
    return actual_rates

def backtest():
    mean_curve = Simulator.main()
    actual_rates = read_SOFR_data()
    print(stats.kstest(mean_curve, actual_rates))
    plt.plot(mean_curve, label='Simulated Mean Curve')
    plt.plot(actual_rates.values, label='Actual SOFR Rates')
    plt.title('Simulated vs Actual Interest Rate Curve')
    plt.xlabel('Time Steps')
    plt.ylabel('Interest Rate')
    plt.legend()
    plt.show()