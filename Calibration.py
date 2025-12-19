import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import Input_Data
import logging

logging.basicConfig(level=logging.INFO)

rates_data = Input_Data.main()
rates_diff = rates_data.diff(-1)
rates_diff = rates_diff.dropna().reset_index(drop=True)
rates_data = rates_data.iloc[1:].dropna().reset_index(drop=True)

# plt.plot(rates_diff)
# plt.title('Differenced Rates')
# plt.xlabel('Time Steps')
# plt.ylabel('Rate Difference')
# plt.show()
# Augmented Dickey-Fuller test for stationarity
adf_result = adfuller(rates_diff, autolag='AIC')

print('ADF Statistic:', adf_result[0])
print('p-value:', adf_result[1])

if adf_result[1] > 0.05:
    logging.warning("The AR(1) series is not stationary. OLS results are unstable")

#OLS Regression to estimate k, theta, sigma

def calibrate_params(rates_diff):
    data = pd.concat([rates_diff, rates_data], axis=1)
    data.columns = ['Delta_rates', 'rates_t-1']
    x = sm.add_constant(data['rates_t-1'])
    y = data['Delta_rates']
    result_OLS = sm.OLS(y, x).fit()
    print(result_OLS.summary())
    
    #delta_r = alpha + beta*r(t-1) + error
    alpha = result_OLS.params['const']
    beta = result_OLS.params['rates_t-1']

    if beta >=0:
        logging.warning("The estimated parameters are not consistent with the Vasicek model assumptions.")

    delta_t = 1/(252)

    theta = alpha/-beta
    k = -beta/delta_t

    residuals = result_OLS.resid
    sigma = np.sqrt(residuals.var()/delta_t)

    return k, theta, sigma


def main():
    k, theta, sigma = calibrate_params(rates_diff)
    print(f'Calibrated Parameters:\nk: {k}\ntheta: {theta}\nsigma: {sigma}')

if __name__ == "__main__":
    main()