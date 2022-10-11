from dataclasses import dataclass

from pandas import DataFrame, Index, Series


@dataclass
class TSNEPlotData:

    utility: Series = None
    features_df: DataFrame = None
    label_index: Index = None
    nolabel_index: Index = None
