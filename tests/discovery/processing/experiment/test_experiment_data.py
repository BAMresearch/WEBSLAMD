import pandas as pd
import numpy as np

from slamd.discovery.processing.experiment.experiment_data import ExperimentData


def _get_experiment_data():
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 103],
        'y': [6, np.nan, np.nan, 9, np.nan, 101],
        'z': [5, np.nan, 3, np.nan, np.nan, 102]
    })

    return ExperimentData(
        dataframe=df,
        target_names=['y', 'z'],
        feature_names=['x']
    )


def test_index_none_labelled():
    data = _get_experiment_data()

    assert tuple(data.index_none_labelled) == (1, 4)


def test_index_partially_labelled():
    data = _get_experiment_data()

    assert tuple(data.index_partially_labelled) == (2, 3)


def test_index_all_labelled():
    data = _get_experiment_data()

    assert tuple(data.index_all_labelled) == (0, 5)


def test_index_predicted():
    data = _get_experiment_data()

    assert tuple(data.index_predicted) == (1, 2, 3, 4)
