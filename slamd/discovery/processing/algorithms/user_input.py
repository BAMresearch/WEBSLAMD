from dataclasses import dataclass, field

# Example user input configuration for the file MaterialsDiscoveryExampleData.csv
# This dataset can be found here:
# https://github.com/BAMresearch/SequentialLearningApp


@dataclass
class UserInput:
    # options=['AI Model (lolo Random Forest)','Statistics-based model (Gaussian Process Regression)'],
    model: str = 'Statistics based model (Gaussian Process Regression)'
    # curiosity (to control the weight of uncertainty):
    curiosity: float = 1.0
    # Features, columns used for training the algorithm
    features: list[str] = field(default_factory=lambda: [
        'SiO2', 'CaO', 'SO3', 'FA (kg/m3)', 'GGBFS (kg/m3)', 'Coarse aggregate (kg/m3)',
        'Fine aggregate (kg/m3)', 'Total aggregates', 'Na2SiO3', 'Na2O (Dry)', 'Sio2 (Dry)', 'Superplasticizer',
        'water -eff'
    ])
    # Target properties
    targets: list[str] = field(default_factory=lambda: ['fc 28-d - Target (MPa)'])
    # Weights for every target property
    target_weights: list[float] = field(default_factory=lambda: [1])
    # Thresholds for every apriori and target property
    target_thresholds: list[float | None] = field(default_factory=lambda: [None])
    # Select for each target property if it should be maximized or minimized
    target_max_or_min: list[str] = field(default_factory=lambda: ['maximize'])
    # A Priori Information
    apriori_columns: list[str] = field(default_factory=lambda: ['CO2 (kg/t) - A-priori Information'])
    # Weights for every fixed target property
    apriori_weights: list[float] = field(default_factory=lambda: [1])
    # Thresholds for apriori properties
    apriori_thresholds: list[float | None] = field(default_factory=lambda: [None])
    # Select for each fixed target property if it should be maximized or minimized
    apriori_max_or_min: list[str] = field(default_factory=lambda: ['minimize'])
