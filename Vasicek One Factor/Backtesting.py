import pandas as pd
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import Input_Data
import Calibration
import logging

logging.basicConfig(level=logging.INFO)

k, theta, sigma = Calibration.calibrate_params(Calibration.rates_diff)
rates_data = Input_Data.main()
delta_t = 1/252  # Daily steps
test_rates = rates_data.iloc[-252:].reset_index(drop=True)
# test_rates = test_rates['Rates'].values

def compute_mu_sigma(k, theta, sigma, test_rates, pointer):
    """
    Compute the mean and standard deviation of the simulated interest rate curve.

    mu_t = r(t)*exp(-k*delta_t) + theta*(1 - exp(-k*delta_t))

    sigma_t = sigma*sqrt((1 - exp(-2*k*delta_t))/(2*k))
    """
    r0 = test_rates['Rates'].iloc[pointer]

    mu_t = r0*(np.exp(-k*delta_t)) + theta*(1 - (np.exp(-k*delta_t)))
    sigma_t = sigma*(np.sqrt((1 - np.exp(-2*k*delta_t))/(2*k)))

    return mu_t, sigma_t

def backtest(test_rates, k, theta, sigma):
    """
    Backtest the Vasicek One Factor model by comparing PIT values to Uniform distribution
    """
    pit = pd.DataFrame(columns = ['Date', 'PIT_Value'])
    for pointer in range(len(test_rates)-1):
        mu_t, sigma_t = compute_mu_sigma(k, theta, sigma, test_rates, pointer)
        r_t1 = test_rates['Rates'].iloc[pointer + 1]
        z_value = (r_t1 - mu_t)/sigma_t
        pit = pd.concat([pit, pd.DataFrame({'Date':test_rates['Effective Date'].iloc[pointer], 'PIT_Value':[scipy.stats.norm.cdf(z_value)]})], ignore_index=True)
    print(stats.kstest(pit['PIT_Value'].values, 'uniform'))  # Kolmogorov-Smirnov test against Uniform distribution
    return pit

def main():
    pit = backtest(test_rates, k, theta, sigma)
    plt.hist(pit['PIT_Value'].values, bins=20, density=True, edgecolor='black')
    plt.axhline(
        y=1.0,
        linestyle='--',
        linewidth=2
    )
    plt.title('PIT Value Distribution vs Uniform Distribution')
    plt.xlabel('PIT Value')
    plt.ylabel('Density')
    plt.show()

if __name__ == "__main__":
    main()