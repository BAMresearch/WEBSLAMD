import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.pipeline import Pipeline

from slamd.discovery.processing.experiment.experiment_data import ExperimentData
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel
from slamd.discovery.processing.experiment.mlmodel.mlmodel_factory import MLModelFactory
from slamd.discovery.processing.experiment.mlmodel.slamd_random_forest import SlamdRandomForest
from slamd.discovery.processing.experiment.mlmodel.tuned_gaussian_process_regressor import TunedGaussianProcessRegressor
from slamd.discovery.processing.experiment.mlmodel.tuned_random_forest import TunedRandomForest


def _get_experiment_data(model):
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 103],
        'y': [6, np.nan, np.nan, 9, np.nan, 101]
    })

    return ExperimentData(
        dataframe=df,
        model=model,
        target_names=['y'],
        feature_names=['x']
    )


def test_mlmodel_factory_returns_correct_model_type():
    models = ExperimentModel.get_all_models()
    expected_types = [GaussianProcessRegressor, SlamdRandomForest, Pipeline, Pipeline]
    assert len(models) == len(expected_types)

    for (model, expected_type) in zip(models, expected_types):
        exp = _get_experiment_data(model)
        result = MLModelFactory.initialize_model(exp)
        assert type(result) == expected_type


def test_mlmodel_factory_returns_correct_model_type_for_tuned_models(client, monkeypatch):
    models = ExperimentModel.get_tuned_models()
    expected_types = [Pipeline, Pipeline]
    assert len(models) == len(expected_types)

    def mock_find_best_model(training_rows, training_labels):
        return Pipeline(('gp2', GaussianProcessRegressor()))

    monkeypatch.setattr(TunedGaussianProcessRegressor, 'find_best_model', mock_find_best_model)
    monkeypatch.setattr(TunedRandomForest, 'find_best_model', mock_find_best_model)

    for (model, expected_type) in zip(models, expected_types):
        exp = _get_experiment_data(model)
        result = MLModelFactory.initialize_model(exp)
        assert type(result) == expected_type
