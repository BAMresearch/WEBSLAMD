from pandas import DataFrame, Index
from dataclasses import dataclass, field

@dataclass
class Experiment:
    dataframe: DataFrame = None
    # Original copy of the data - no transformations applied. TODO necessary?
    dataframe_orig: DataFrame = None
    model: str = None # TODO rename
    curiosity: float = None

    target_names: list[str] = field(default_factory=lambda: [''])
    target_weights: list[float] = field(default_factory=lambda: [0])
    target_thresholds: list[float] = field(default_factory=lambda: [0])
    target_max_or_min: list[str] = field(default_factory=lambda: [''])

    apriori_names: list[str] = field(default_factory=lambda: [''])
    apriori_weights: list[float] = field(default_factory=lambda: [0])
    apriori_thresholds: list[float] = field(default_factory=lambda: [0])
    apriori_max_or_min: list[str] = field(default_factory=lambda: [''])

    feature_names: list[str] = field(default_factory=lambda: [''])

    labelled_index: Index = None
    unlabelled_index: Index = None

    @property
    def features_df(self):
        return self.dataframe[self.feature_names]

    @property
    def targets_df(self):
        return self.dataframe[self.target_names]

    @property
    def apriori_df(self):
        return self.dataframe[self.apriori_names]

    @property
    def label_index(self):
        # TODO Old version: checks only for the first column
        # Selects the rows that have a label for the first target
        # These have a null value in the corresponding column
        # self.prediction_index = pd.isnull(self.dataframe[[self.targets[0]]]).to_numpy().nonzero()[0]
        # TODO New version: Checks for all columns. Verify this is correct
        return self.targets_df.notnull().all(axis=1)

    @property
    def nolabel_index(self):
        return self.dataframe.index.difference(self.label_index)

