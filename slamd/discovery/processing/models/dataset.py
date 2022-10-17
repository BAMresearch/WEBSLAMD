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

    @classmethod
    def from_dict(cls, dictionary):
        dataset = cls(
            name=dictionary['name'],
            target_columns=dictionary['target_columns'],
        )
        dataset.dataframe = pd.DataFrame.from_dict(dictionary['dataframe'])
        dataset.dataframe = dataset.dataframe.reset_index(drop=True)

        return dataset
