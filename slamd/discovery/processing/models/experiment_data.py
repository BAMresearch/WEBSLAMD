import pandas as pd
from pandas import DataFrame, Index
from dataclasses import dataclass, field

@dataclass
class ExperimentData:
    # TODO Should novelty and utility be written into this?
    #  => Do that, and turn novelty into series
    # TODO Figure out if orig_data should contain dropped apriori or not. It currently *does*.
    # TODO Unit tests for validate_experiment?
    # TODO (Future -> Jira) Better unit tests for run experiment
    # TODO (Future -> Jira) Think of more sensible errors we could throw
    # TODO (Future -> Jira) Should maxmin be converted to -1, 1?
    # TODO (Future -> Jira) Make calculation of nolabel index more robust / already possible due to validation?
    # TODO (Future -> Jira) Turn filter apriori into part of (no)label_index
    # TODO (Future -> Jira) Decided if NaN should drop rows or columns. Currently drops columns
    #  -> would simply be exp.dataframe.dropna(inplace=True, subset=exp.feature_names)
    #
    orig_data: DataFrame = None
    dataframe: DataFrame = None
    model: str = None
    curiosity: float = None

    target_names: list[str] = field(default_factory=lambda: [])
    target_weights: list[float] = field(default_factory=lambda: [])
    target_thresholds: list[float | None] = field(default_factory=lambda: [])
    target_max_or_min: list[str] = field(default_factory=lambda: [])

    apriori_names: list[str] = field(default_factory=lambda: [])
    apriori_weights: list[float] = field(default_factory=lambda: [])
    apriori_thresholds: list[float | None] = field(default_factory=lambda: [])
    apriori_max_or_min: list[str] = field(default_factory=lambda: [])

    feature_names: list[str] = field(default_factory=lambda: [])

    labelled_index: Index = None
    unlabelled_index: Index = None

    prediction: DataFrame = None
    uncertainty: DataFrame = None
    utility: DataFrame = None
    novelty: DataFrame = None


    def __post_init__(self):
        self.orig_data = self.dataframe.copy()
        self.dataframe = self.dataframe.copy()  # otherwise, dataset object in session gets overwritten

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
    def nolabel_index(self):
        # TODO
        return pd.isnull(self.dataframe[[self.target_names[0]]]).to_numpy().nonzero()[0]

    @property
    def label_index(self):
        # TODO replace difference
        return self.dataframe.index.difference(self.nolabel_index)

