from dataclasses import dataclass, field


@dataclass
class UserInput:
    # curiosity (to control the weight of uncertainty):
    curiosity: float = 1.0
    # options=['AI-Model (lolo Random Forrest)','Statistics based model (Gaussian Process Regression)'],
    model: str = 'Statistics based model (Gaussian Process Regression)'
    # σ Factor (to control the weight of uncertainty):
    sigma_factor: float = 1
    # Prediction quantile for distance-based utility (smaller values recommended for weak predictors):
    prediction_quantile_distance: float = 1
    # Target properties
    targets: list[str] = field(default_factory=lambda: ['fc 28-d - Target (MPa)'])
    # Weights for every target property
    target_weights: list[int] = field(default_factory=lambda: [1])
    # Select for each target property if it should be maximized or minimized
    target_max_or_min: list[str] = field(default_factory=lambda: ['maximize'])
    # A Priori Information
    fixed_targets: list[str] = field(default_factory=lambda: ['CO2 (kg/t) - A-priori Information'])
    # Weights for every fixed target property
    fixed_target_weights: list[int] = field(default_factory=lambda: [1])
    # Select for each fixed target property if it should be maximized or minimized
    fixed_target_max_or_min: list[str] = field(default_factory=lambda: ['minimize'])
    # Features, columns used for training the algorithm
    features: list[str] = field(default_factory=lambda: [
        'SiO2', 'CaO', 'SO3', 'FA (kg/m3)', 'GGBFS (kg/m3)', 'Coarse aggregate (kg/m3)',
        'Fine aggregate (kg/m3)', 'Total aggregates', 'Na2SiO3', 'Na2O (Dry)', 'Sio2 (Dry)', 'Superplasticizer',
        'water -eff'
    ])
