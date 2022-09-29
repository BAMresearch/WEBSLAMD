import pandas as pd
import numpy as np

from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment
from slamd.discovery.processing.models.experiment_data import ExperimentData


def test_clip_predictions_for_one_target_no_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['max'], target_thresholds=[None])
    clipped_prediction = DiscoveryExperiment.clip_prediction(experiment)

    assert np.array_equal(clipped_prediction, input_prediction)


def test_clip_predictions_for_one_target_min_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['min'], target_thresholds=[5])
    clipped_prediction = DiscoveryExperiment.clip_prediction(experiment)

    expected_output = pd.DataFrame({'x': [5, 5, 5, 5, 5, 5, 6, 7, 8, 9]})

    # Using pd.DataFrame.equals does not work - potentially because of dtypes
    assert np.array_equal(clipped_prediction.values, expected_output.values)


def test_clip_predictions_for_one_target_max_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['max'], target_thresholds=[5])
    clipped_prediction = DiscoveryExperiment.clip_prediction(experiment)

    expected_output = pd.DataFrame({'x': [0, 1, 2, 3, 4, 5, 5, 5, 5, 5]})

    assert np.array_equal(clipped_prediction.values, expected_output.values)


def test_clip_predictions_for_two_targets_maxmin_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({
        'x': [0, 1, 2, 3, 4, 5, 6, 7],
        'y': [0, 1, 2, 3, 4, 5, 6, 7],
    })
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x', 'y'], prediction=input_prediction,
                                target_max_or_min=['max', 'min'], target_thresholds=[4, 6])
    clipped_prediction = DiscoveryExperiment.clip_prediction(experiment)

    expected_output = pd.DataFrame({
        'x': [0, 1, 2, 3, 4, 4, 4, 4],
        'y': [6, 6, 6, 6, 6, 6, 6, 7],
    })

    assert np.array_equal(expected_output.values, clipped_prediction.values)


def test_clip_predictions_for_two_targets_partial_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({
        'x': [0, 1, 2, 3, 4, 5, 6, 7],
        'y': [0, 1, 2, 3, 4, 5, 6, 7],
    })
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x', 'y'], prediction=input_prediction,
                                target_max_or_min=['max', 'min'], target_thresholds=[4, None])
    clipped_prediction = DiscoveryExperiment.clip_prediction(experiment)

    expected_output = pd.DataFrame({
        'x': [0, 1, 2, 3, 4, 4, 4, 4],
        'y': [0, 1, 2, 3, 4, 5, 6, 7],
    })

    assert np.array_equal(expected_output.values, clipped_prediction.values)


def test_filter_apriori_thresholds():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': [], 'y': [], 'z': [], 'u': [], 'v': [], 'w': []}), model="", curiosity=1, features=[],
        targets=['x', 'y'], target_weights=[1, 1], target_thresholds=[None, None], target_max_or_min=['max', 'min'],
        apriori_columns=['u', 'v'], apriori_thresholds=[4, 5], apriori_weights=[1, 1], apriori_max_or_min=['max', 'min']
    )

    df = experiment.dataframe
    df['u'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['v'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['x'] = [np.nan, np.nan, np.nan, 4, np.nan, np.nan, 7, 8]
    df['y'] = [1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 8]

    result = experiment.filter_apriori_with_thresholds(df)

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

    DiscoveryExperiment._encode_categoricals(experiment)

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

    DiscoveryExperiment._encode_categoricals(experiment)

    assert np.array_equal(experiment.dataframe['u'].values, input_df['u'].values)
    assert np.array_equal(experiment.dataframe['v'].values, input_df['v'].values)


def test_encode_categoricals_empty():
    input_df = pd.DataFrame()

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    DiscoveryExperiment._encode_categoricals(experiment)

    assert input_df.empty