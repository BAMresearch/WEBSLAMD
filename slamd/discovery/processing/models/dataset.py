from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class Dataset:
    name: str = None
    dataframe: DataFrame = None
