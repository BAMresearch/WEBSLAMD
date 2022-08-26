import pandas as pd
from dataclasses import dataclass

from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment


@dataclass
class UserInput:
    curiosity: float = 1.0
    model: str = 'Statistics based model (Gaussian Process Regression)'
    strategy: str = 'MEI (exploit)'
    sigma_factor: float = 1
    prediction_quantile: float = 1


class LearningModel:

    @classmethod
    def run(cls):
        # Run the model on the given dataset
        print('Running....')
        user_input = UserInput(curiosity=2.0)
        dataframe = pd.read_csv('MaterialsDiscoveryExampleData.csv')
        experiment = DiscoveryExperiment(dataframe, user_input.model, user_input.strategy,
                                         user_input.sigma_factor, user_input.prediction_quantile)

        result = experiment.start_learning()
        print(result)


if __name__ == '__main__':
    LearningModel.run()
