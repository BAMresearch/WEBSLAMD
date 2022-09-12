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
