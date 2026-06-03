import pandas as pd
import pathlib

class dataloader:
    """
    Generic Loader Class to load data from a given path. The path is expected to be a CSV file. 
    The load method reads the CSV file and returns a pandas DataFrame.
    """
    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    @classmethod
    def load(cls, path: str) -> pd.DataFrame:
        return pd.read_csv(path)