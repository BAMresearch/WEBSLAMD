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


class LearningModel:

    @classmethod
    def run(cls):
        # Run the model on the given dataset
        print('Running....')
        user_input = UserInput(curiosity=2.0)
        dataframe = pd.read_csv('MaterialsDiscoveryExampleData.csv')
        dataframe.apply(pd.to_numeric, errors='ignore')
        experiment = DiscoveryExperiment(dataframe, user_input.model, user_input.strategy,
                                         user_input.sigma_factor, user_input.prediction_quantile_distance)

        result = experiment.start_learning()
        print(result)


if __name__ == '__main__':
    LearningModel.run()
