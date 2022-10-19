from enum import Enum


class ExperimentModel(Enum):
    GAUSSIAN_PROCESS = 'Statistics-based model (Gaussian Process Regression)'
    RANDOM_FOREST = 'AI Model (lolo Random Forest)'
    PCA_GAUSSIAN_PROCESS = 'Gaussian Process with PCA'
    PCA_RANDOM_FOREST = 'Random Forest with PCA'
    TUNED_GAUSSIAN_PROCESS = 'Tuned Gaussian Process'
    TUNED_RANDOM_FOREST = 'Tuned Random Forest'

    @classmethod
    def get_all_models(cls):
        return [e.value for e in ExperimentModel]
