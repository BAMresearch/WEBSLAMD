from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class Prediction:
    dataset_used_for_prediction: str = ''
    dataframe: DataFrame = None
    metadata: dict = None
