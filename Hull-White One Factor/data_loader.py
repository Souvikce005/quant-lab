import pandas as pd
import pathlib

class DataLoader:
    """
    Generic Loader Class to load data from a given path. The path is expected to be an Excel file. 
    The load method reads the Excel file and returns a pandas DataFrame.
    """
    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    @classmethod
    def load(cls, path: str) -> pd.DataFrame:
        return pd.read_excel(path)