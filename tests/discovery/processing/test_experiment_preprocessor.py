import numpy as np
import pandas as pd

from slamd.discovery.processing.algorithms.experiment_preprocessor import ExperimentPreprocessor
from slamd.discovery.processing.models.experiment_data import ExperimentData


def test_filter_apriori_thresholds():
    df = pd.DataFrame()
    df['u'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['v'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['x'] = [np.nan, np.nan, np.nan, 4, np.nan, np.nan, 7, 8]
    df['y'] = [1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 8]

    experiment = ExperimentData(dataframe=df, target_names=['x', 'y'], apriori_names=['u', 'v'],
                                apriori_thresholds=[4, 5], apriori_max_or_min=['max', 'min'])

    ExperimentPreprocessor._filter_apriori_with_thresholds(experiment)
    result = experiment.dataframe

    assert np.array_equal(result['u'].values, np.array([1, 4, 5, 7, 8]))
    assert np.array_equal(result['v'].values, np.array([1, 4, 5, 7, 8]))
    assert np.array_equal(np.nan_to_num(result['x'].values), np.array([0, 4, 0, 7, 8]))
    assert np.array_equal(np.nan_to_num(result['y'].values), np.array([1, 0, 0, 0, 8]))


def test_encode_categoricals_multiple():
    input_df = pd.DataFrame({
        'u': [1, 2, 3],
        'v': [1.0, 2.3, 4.5],
        'w': ['a', 'b', 'c'],
        'x': ['asdf', 'qwer', 'yxcv']
    })

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor._encode_categoricals(experiment)

    assert np.array_equal(experiment.dataframe['u'].values, input_df['u'].values)
    assert np.array_equal(experiment.dataframe['v'].values, input_df['v'].values)
    assert np.array_equal(experiment.dataframe['w'].values, np.array([0, 1, 2]))
    assert np.array_equal(experiment.dataframe['x'].values, np.array([0, 1, 2]))


def test_encode_categoricals_none():
    input_df = pd.DataFrame({
        'u': [1, 2, 3],
        'v': [1.0, 2.3, 4.5],
    })

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor._encode_categoricals(experiment)

    assert np.array_equal(experiment.dataframe['u'].values, input_df['u'].values)
    assert np.array_equal(experiment.dataframe['v'].values, input_df['v'].values)


def test_encode_categoricals_empty():
    input_df = pd.DataFrame()

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor._encode_categoricals(experiment)

    assert experiment.dataframe.empty
