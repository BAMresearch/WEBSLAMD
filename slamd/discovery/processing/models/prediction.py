from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class Prediction:
    dataframe: DataFrame = None
    metadata: dict = None
