from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class Dataset:
    name: str = None
    target_columns: list[str] = None
    dataframe: DataFrame = None

    @property
    def columns(self):
        return list(self.dataframe.columns)

    def add_target(self, target_name):
        if self.target_columns:
            self.target_columns.append(target_name)
        else:
            self.target_columns = [target_name]
