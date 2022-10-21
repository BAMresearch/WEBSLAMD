from enum import Enum
import os


class ExperimentModel(Enum):
    GAUSSIAN_PROCESS = 'Gaussian Process Regression (Statistics-based model)'
    RANDOM_FOREST = 'lolo Random Forest (AI model)'
    PCA_GAUSSIAN_PROCESS = 'Gaussian Process Regression with PCA'
    PCA_RANDOM_FOREST = 'lolo Random Forest with PCA'
    TUNED_GAUSSIAN_PROCESS = 'tuned Gaussian Process Regression (under development)'
    TUNED_RANDOM_FOREST = 'tuned lolo Random Forest (under development)'

    @classmethod
    def get_all_models(cls):
        if os.getenv('FLASK_ENV') == 'development':
            return [e.value for e in ExperimentModel]
        return [e.value for e in ExperimentModel if e.value not in cls.get_tuned_models()]

    @ classmethod
    def get_tuned_models(cls):
        return [ExperimentModel.TUNED_GAUSSIAN_PROCESS.value, ExperimentModel.TUNED_RANDOM_FOREST.value]
