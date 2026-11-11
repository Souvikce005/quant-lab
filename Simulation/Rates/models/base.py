from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, name, **kwargs):
        self.name = name
        self.params = kwargs

    def get_params(self):
        return self.params

    def set_params(self, **kwargs):
        self.params.update(kwargs)
