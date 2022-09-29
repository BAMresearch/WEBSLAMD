import pandas as pd
from pandas import DataFrame, Index
from dataclasses import dataclass, field

@dataclass
class ExperimentData:
    orig_data: DataFrame = None # TODO still contains dropped apriori
    dataframe: DataFrame = None
    model: str = None # TODO rename
    curiosity: float = None

    # TODO Defaults: List of empty str or empty list?
    target_names: list[str] = field(default_factory=lambda: [''])
    target_weights: list[float] = field(default_factory=lambda: [1])
    target_thresholds: list[float | None] = field(default_factory=lambda: [None])
    target_max_or_min: list[str] = field(default_factory=lambda: [''])

    apriori_names: list[str] = field(default_factory=lambda: [''])
    apriori_weights: list[float] = field(default_factory=lambda: [1])
    apriori_thresholds: list[float | None] = field(default_factory=lambda: [None])
    apriori_max_or_min: list[str] = field(default_factory=lambda: [''])

    feature_names: list[str] = field(default_factory=lambda: [''])

    labelled_index: Index = None
    unlabelled_index: Index = None

    uncertainty: DataFrame = None
    prediction: DataFrame = None
    novelty_factor = None  # TODO Series?

    def __post_init__(self):
        self.orig_data = self.dataframe.copy()

    @property
    def features_df(self):
        return self.dataframe[self.feature_names]

    @property
    def targets_df(self):
        return self.dataframe[self.target_names]

    @property
    def apriori_df(self):
        return self.dataframe[self.apriori_names]

    # TODO it is very likely sample/prediction were mixed up here due to the confusing naming
    #  sample index -> marks data used for training. has labels.
    #  prediction index -> marks data used for prediction. has no labels.
    #  Verify.
    # return self.targets_df.notnull().all(axis=1)
    @property
    def label_index(self):
        return self.dataframe.index.difference(self.nolabel_index)

    @property
    def nolabel_index(self):
        return pd.isnull(self.dataframe[[self.target_names[0]]]).to_numpy().nonzero()[0]
    # def _update_prediction_index(self):
    #     # Selects the rows that have a label for the first target TODO should be "no label"?
    #     # These have a null value in the corresponding column
    #     self.prediction_index = pd.isnull(self.dataframe[[self.targets[0]]]).to_numpy().nonzero()[0]
    #
    # def _update_sample_index(self):
    #     # Inverse of prediction index - The rows with labels (the training set) are the rest of the rows
    #     self.sample_index = self.dataframe.index.difference(self.prediction_index)

