from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass


@dataclass
class Model(ABC):
    PARAM_NAMES: tuple[str, ...] = ()

    name: str
    params: dict[str, float] = None

    def __post_init__(self) -> None:
        if self.params is None:
            self.params = {}
        self.set_params(**self.params)

    def get_params(self) -> dict[str, float]:
        return dict(self.params)

    def set_params(self, **params: float) -> None:
        unknown = set(params) - set(self.PARAM_NAMES)
        if unknown:
            raise ValueError(f"Unknown parameters: {unknown}")
        self.params.update(params)
        self.validate_params()

    @abstractmethod
    def validate_params(self) -> None: ...

    @abstractmethod
    def simulate(self, times: np.ndarray, n_paths: int,
                 rng: np.random.Generator) -> np.ndarray: ...

    @abstractmethod
    def discount_factor(self, t: float, T: float,
                        state: np.ndarray) -> np.ndarray: ...
