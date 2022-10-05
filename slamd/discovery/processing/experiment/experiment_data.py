from pandas import DataFrame, Index
from dataclasses import dataclass, field

@dataclass
class ExperimentData:
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
        return self.dataframe.index[self.targets_df.isnull().all(axis=1)]

    @property
    def label_index(self):
        return self.dataframe.index[self.targets_df.notnull().all(axis=1)]

