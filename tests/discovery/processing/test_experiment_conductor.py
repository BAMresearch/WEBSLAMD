import pandas as pd
import numpy as np

from slamd.discovery.processing.experiment.experiment_conductor import ExperimentConductor
from slamd.discovery.processing.experiment.experiment_data import ExperimentData


def test_clip_predictions_for_one_target_no_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['max'], target_thresholds=[None])
    clipped_prediction = ExperimentConductor.clip_prediction(experiment)

    assert np.array_equal(clipped_prediction, input_prediction)


def test_clip_predictions_for_one_target_min_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['min'], target_thresholds=[5])
    clipped_prediction = ExperimentConductor.clip_prediction(experiment)

    expected_output = pd.DataFrame({'x': [5, 5, 5, 5, 5, 5, 6, 7, 8, 9]})

    # Using pd.DataFrame.equals does not work - potentially because of dtypes
    assert np.array_equal(clipped_prediction.values, expected_output.values)


def test_clip_predictions_for_one_target_max_threshold():
    dummy_df = pd.DataFrame()
    input_prediction = pd.DataFrame({'x': np.arange(10)})
    experiment = ExperimentData(dataframe=dummy_df, target_names=['x'], prediction=input_prediction,
                                target_max_or_min=['max'], target_thresholds=[5])
    clipped_prediction = ExperimentConductor.clip_prediction(experiment)

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
    clipped_prediction = ExperimentConductor.clip_prediction(experiment)

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
    clipped_prediction = ExperimentConductor.clip_prediction(experiment)

    expected_output = pd.DataFrame({
        'x': [0, 1, 2, 3, 4, 4, 4, 4],
        'y': [0, 1, 2, 3, 4, 5, 6, 7],
    })

    assert np.array_equal(expected_output.values, clipped_prediction.values)
