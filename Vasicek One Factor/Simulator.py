import numpy as np
import pandas as pd
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import Calibration
import logging
import Input_Data

""" 
Vasicek Model Discretized: 

dr = k(theta - r)dt + sigma*dw

r(t+1) = r(t) + k(theta - r(t))*delta_t + sigma*sqrt(delta_t)*e - Euler Maruyama Discretization 

"""

logging.basicConfig(level=logging.INFO)

def random_generator(sim_period, n_paths): 
    shocks = np.random.default_rng(seed=42).normal(0,1, (sim_period, n_paths))
    return shocks

def simulate_paths(r0, k, theta, sigma, delta_t, sim_period, n_paths):

    random_shocks = random_generator(sim_period, n_paths)

    rates = np.zeros((sim_period + 1, n_paths))
    rates[0] = r0
    for i in range(sim_period): 
        rates[i+1] = rates[i] + k*(theta - rates[i])*delta_t + sigma*np.sqrt(delta_t)*random_shocks[i]
    return rates

def main():
    r0 = 0.044
    k, theta, sigma = Calibration.calibrate_params(Calibration.rates_diff)
    print(k, theta, sigma)
    delta_t = 1/252
    sim_period = 30
    n_paths = 10000
    rates = simulate_paths(r0, k, theta, sigma, delta_t, sim_period, n_paths)
    mean_curve = np.mean(rates, axis = 1)
    return mean_curve

if __name__ == "__main__":
    main()
