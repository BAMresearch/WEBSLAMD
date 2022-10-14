from dataclasses import dataclass

from pandas import DataFrame, Index, Series


@dataclass
class TSNEPlotData:

    utility: Series = None
    features_df: DataFrame = None
    index_all_labelled: Index = None
    index_none_labelled: Index = None
