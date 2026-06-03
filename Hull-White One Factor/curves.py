from cmath import exp

import pandas as pd
from scipy.interpolate import CubicSpline as cubicinterp

class Curve:
    def __init__(self):
        pass
    
    @classmethod
    def get_discount_factor(cls, rates: pd.DataFrame) -> float:
        # Discount factor calculation using zero rates
        return exp(-rates['zero_rate'] * rates['maturity'])
    
    @classmethod
    def interpolate_rate(cls, t: float, rates: pd.DataFrame) -> float:
        # Cubic spline interpolation
        f = cubicinterp(rates['maturity'], rates['zero_rate'])
        return f(t)
    
    @classmethod
    def get_forward_rate(cls, t1: float, t2: float, rates: pd.DataFrame) -> float:
        # Forward curve construction
        df1 = cls.get_discount_factor(rates[rates['maturity'] == t1])
        df2 = cls.get_discount_factor(rates[rates['maturity'] == t2])
        return (df1 / df2 - 1) / (t2 - t1)