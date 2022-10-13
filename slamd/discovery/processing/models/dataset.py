import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass, field


@dataclass
class Dataset:
    name: str = None
    target_columns: list[str] = field(default_factory=lambda: [])
    dataframe: DataFrame = None

    @property
    def columns(self):
        return list(self.dataframe.columns)

    def to_dict(self):
        return {
            'name': self.name,
            'target_columns': self.target_columns,
            'dataframe': self.dataframe.to_dict()
        }

    def from_dict(self, dictionary):
        self.name = dictionary['name']
        self.target_columns = dictionary['target_columns']
        self.dataframe = pd.DataFrame.from_dict(dictionary['dataframe'])
        self.dataframe = self.dataframe.reset_index(drop=True)
