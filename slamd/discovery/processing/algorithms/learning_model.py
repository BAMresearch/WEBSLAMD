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
            dataframe, user_input.model, user_input.strategy, user_input.sigma_factor,
            user_input.prediction_quantile_distance, user_input.targets, user_input.target_weights, user_input.target_max_or_min, user_input.fixed_targets,
            user_input.fixed_target_weights, user_input.fixed_target_max_or_min, user_input.features
        )

        result = experiment.start_learning()
        print(result)


if __name__ == '__main__':
    LearningModel.run()
