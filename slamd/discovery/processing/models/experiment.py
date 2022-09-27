from pandas import DataFrame
from dataclasses import dataclass, field

@dataclass
class Experiment:
    dataframe: DataFrame = None
    # Original copy of the data - no transformations applied. TODO necessary?
    dataframe_orig: DataFrame = None
    model: str = None
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

