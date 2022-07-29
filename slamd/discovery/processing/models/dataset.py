from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class Dataset:
    name: str = None
    dataframe: DataFrame = None

    @property
    def columns(self):
        return self.dataframe.columns
