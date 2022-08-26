import pandas as pd
from dataclasses import dataclass

from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment


@dataclass
class UserInput:
    # curiosity (to control the weight of uncertainty):
    curiosity: float = 1.0
    # options=['AI-Model (lolo Random Forrest)','Statistics based model (Gaussian Process Regression)'],
    model: str = 'Statistics based model (Gaussian Process Regression)'
    # options=['MEI (exploit)','MU (explore)','MLI (explore & exploit)','MEID (exploit)','MLID (explore & exploit)'],
    strategy: str = 'MEI (exploit)'
    # σ Factor (to controll the weigth of uncertainty):
    sigma_factor: float = 1
    # Prediction quantile for distance-based utility (smaller values recommended for weak predictors):
    prediction_quantile_distance: float = 1
    # Target properties
    targets: list[str] = ['fc 28-d - Target (MPa)']
    # A Priori Information
    fixed_targets: list[str] = ['CO2 (kg/t) - A-priori Information']
    # Features, columns used for training the algorithm
    features: list[str] = [
        'Idx_Sample', 'SiO2', 'CaO', 'SO3', 'FA (kg/m3)', 'GGBFS (kg/m3)', 'Coarse aggregate (kg/m3)',
        'Fine aggregate (kg/m3)', 'Total aggregates', 'Na2SiO3', 'Na2O (Dry)', 'Sio2 (Dry)', 'Superplasticizer',
        'water -eff'
    ]


class LearningModel:

    @classmethod
    def run(cls):
        # Run the model on the given dataset
        print('Running....')
        user_input = UserInput(curiosity=2.0)
        dataframe = pd.read_csv('MaterialsDiscoveryExampleData.csv')
        dataframe.apply(pd.to_numeric, errors='ignore')
        experiment = DiscoveryExperiment(dataframe, user_input.model, user_input.strategy,
                                         user_input.sigma_factor, user_input.prediction_quantile_distance,
                                         user_input.targets)

        result = experiment.start_learning()
        print(result)


if __name__ == '__main__':
    LearningModel.run()
