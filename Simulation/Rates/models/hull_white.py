from .base import Model
import numpy as np


class HullWhiteOneFactor(Model):
    PARAM_NAMES = ("a", "sigma", "theta")

    def validate_params(self) -> None:
        a = self.params.get("a")
        sigma = self.params.get("sigma")
        theta = self.params.get("theta")
        if a is None or a <= 0:
            raise ValueError("Parameter 'a' must be positive")
        if sigma is None or sigma <= 0:
            raise ValueError("Parameter 'sigma' must be positive")
        if theta is None:
            raise ValueError("theta must be provided")
        self.validate_finite_parameters(a, sigma)

    def validate_finite_parameters(self, a, sigma):
        if not np.isfinite(a) or not np.isfinite(sigma):
            raise ValueError("Parameters 'a' and 'sigma' must be finite numbers")

    def simulate(self, times: np.ndarray, n_paths: int,
                 rng: np.random.Generator) -> np.ndarray:
        pass