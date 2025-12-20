import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import Input_Data
import logging

logging.basicConfig(level=logging.INFO)

rates_data = Input_Data.main()
rates_data = rates_data.iloc[0:251]
rates_diff = rates_data['Rates'] - rates_data['Rates'].shift(-1)
rates_lag = rates_data['Rates'].shift(-1)

def calibrate_params(rates_diff):
    data = pd.concat([rates_diff, rates_lag], axis=1).dropna()
    data.columns = ['Delta_rates', 'rates_t']
    x = sm.add_constant(data['rates_t'])
    y = data['Delta_rates']
    result_OLS = sm.OLS(y, x).fit()
    print(result_OLS.summary())
    
    #delta_r = alpha + beta*r(t-1) + error
    alpha = result_OLS.params['const']
    beta = result_OLS.params['rates_t']

    if beta >=0:
        logging.warning("The estimated parameters are not consistent with the Vasicek model assumptions.")

    delta_t = 1/252

    theta = alpha/-beta
    k = -beta/delta_t

    residuals = result_OLS.resid
    sigma = np.sqrt(residuals.var(ddof=1)/delta_t)

    return k, theta, sigma


def main():
    k, theta, sigma = calibrate_params(rates_diff)
    print(f'Calibrated Parameters:\nk: {k}\ntheta: {theta}\nsigma: {sigma}')

if __name__ == "__main__":
    main()