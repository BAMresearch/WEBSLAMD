from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.experiment.mlmodel.slamd_random_forest import SlamdRandomForest
from slamd.discovery.processing.experiment.mlmodel.tuned_gaussian_process_regressor import TunedGaussianProcessRegressor
from slamd.discovery.processing.experiment.mlmodel.tuned_random_forest import TunedRandomForest
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel


class MLModelFactory:

    @classmethod
    def initialize_model(cls, exp):
        """
        Initialize the model given by the user. Return a sklearn Regressor.
        The model must be one of the entries defined in ExperimentModel.
        """
        if exp.model == ExperimentModel.RANDOM_FOREST.value:
            regressor = SlamdRandomForest()
        elif exp.model == ExperimentModel.GAUSSIAN_PROCESS.value:
            # Hyperparameters from previous implementation of the app (Jupyter notebook).
            kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
            regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, random_state=42)
        elif exp.model == ExperimentModel.PCA_GAUSSIAN_PROCESS.value:
            # These hyperparameters were found to be potentially interesting by running local experiments.
            predictor = GaussianProcessRegressor(n_restarts_optimizer=3, random_state=42)
            pca = PCA(n_components=0.99)
            regressor = Pipeline([('pca', pca), ('pred', predictor)])
        elif exp.model == ExperimentModel.PCA_RANDOM_FOREST.value:
            predictor = SlamdRandomForest()
            pca = PCA(n_components=0.99)
            regressor = Pipeline([('pca', pca), ('pred', predictor)])
        elif exp.model in ExperimentModel.get_tuned_models():
            # These models only support one target for now. Validated user input in ExperimentPreprocessor.
            target = exp.target_names[0]
            index_labelled = exp.targets_df.index[exp.targets_df[target].notnull()]
            training_rows = exp.features_df.loc[index_labelled].values
            training_labels = exp.targets_df.loc[index_labelled, target].values.reshape(-1, 1)

            if exp.model == ExperimentModel.TUNED_GAUSSIAN_PROCESS.value:
                regressor = TunedGaussianProcessRegressor.find_best_model(training_rows, training_labels)
            else:
                regressor = TunedRandomForest.find_best_model(training_rows, training_labels)
        else:
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        return regressor
