from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class TSNEPlotData:

    utility: DataFrame = None
    features_df: DataFrame = None
    label_index: DataFrame = None
    nolabel_index: DataFrame = None
