import pandas as pd


from user_input import UserInput
from discovery_experiment import DiscoveryExperiment


class LearningModel:

    @classmethod
    def run(cls):
        # Run the model on the given dataset
        print('Running....')
        user_input = UserInput()
        dataframe = pd.read_csv('MaterialsDiscoveryExampleData.csv')
        dataframe.apply(pd.to_numeric, errors='ignore')
        experiment = DiscoveryExperiment(
            dataframe=dataframe,
            model=user_input.model,
            sigma=user_input.sigma_factor,
            distance=user_input.prediction_quantile_distance,
            features=user_input.features,
            targets=user_input.targets,
            target_weights=user_input.target_weights,
            target_max_or_min=user_input.target_max_or_min,
            fixed_targets=user_input.fixed_targets,
            fixed_target_weights=user_input.fixed_target_weights,
            fixed_target_max_or_min=user_input.fixed_target_max_or_min
        )

        result = experiment.start_learning()
        print(result)


if __name__ == '__main__':
    LearningModel.run()
