from cmath import exp

import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline

class Curve:

    def __init__(self, data):

        self.data = data

        self.maturity = data['maturity'].values
        self.zero_rate = data['zero_rate'].values

        self.discount_factor_nodes = np.exp(
            -self.zero_rate*self.maturity
        )

        self.log_df_spline = CubicSpline(
            self.maturity,
            np.log(self.discount_factor_nodes)
        )

    def discount_factor(self,t):
        return np.exp(
            self.log_df_spline(t)
        )

    def zero_rate(self,t):
        return (
            -np.log(
                self.discount_factor(t)
            )/t
        )

    def forward_rate(self,t):
        return -self.log_df_spline.derivative()(t)