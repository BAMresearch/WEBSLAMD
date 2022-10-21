from dataclasses import dataclass, field
from pandas import DataFrame


@dataclass
class Dataset:
    name: str = None
    target_columns: list[str] = field(default_factory=list)
    dataframe: DataFrame = None

    @property
    def columns(self):
        return list(self.dataframe.columns)
