import pandas as pd
import numpy as np

from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment


def test_clip_predictions_for_one_target_no_threshold():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': []}), model="", curiosity=1, features=[], targets=['x'], target_weights=[1],
        target_thresholds=[None],
        target_max_or_min=['max'], apriori_thresholds=[], apriori_columns=[], apriori_weights=[],
        apriori_max_or_min=[]
    )

    input_prediction = np.arange(10)
    experiment.prediction = input_prediction
    clipped_prediction = experiment.clip_predictions()

    assert clipped_prediction.all() == input_prediction.all()


def test_clip_predictions_for_one_target_min_threshold():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': []}), model="", curiosity=1, features=[], targets=['x'], target_weights=[1],
        target_thresholds=[5],
        target_max_or_min=['min'], apriori_thresholds=[], apriori_columns=[], apriori_weights=[],
        apriori_max_or_min=[]
    )

    input_prediction = np.arange(10)
    experiment.prediction = input_prediction
    clipped_prediction = experiment.clip_predictions()

    assert clipped_prediction.all() == np.array([5, 5, 5, 5, 5, 5, 6, 7, 8, 9, 10]).all()


def test_clip_predictions_for_one_target_max_threshold():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': []}), model="", curiosity=1, features=[], targets=['x'], target_weights=[1],
        target_thresholds=[5],
        target_max_or_min=['max'], apriori_thresholds=[], apriori_columns=[], apriori_weights=[],
        apriori_max_or_min=[]
    )

    input_prediction = np.arange(10)
    experiment.prediction = input_prediction
    clipped_prediction = experiment.clip_predictions()

    assert clipped_prediction.all() == np.array([0, 1, 2, 3, 4, 5, 5, 5, 5, 5]).all()


def test_clip_predictions_for_two_targets_maxmin_threshold():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': [], 'y': []}), model="", curiosity=1, features=[], targets=['x', 'y'],
        target_weights=[1, 1], target_thresholds=[4, 6],
        target_max_or_min=['max', 'min'], apriori_thresholds=[], apriori_columns=[], apriori_weights=[],
        apriori_max_or_min=[]
    )

    input_prediction = np.array(
        [
            [0, 1, 2, 3, 4, 5, 6, 7],
            [0, 1, 2, 3, 4, 5, 6, 7],
        ]
    )
    expected_output = np.array(
        [
            [0, 1, 2, 3, 4, 4, 4, 4],
            [6, 6, 6, 6, 6, 6, 6, 7],
        ]
    )
    experiment.prediction = input_prediction
    clipped_prediction = experiment.clip_predictions()

    assert clipped_prediction.all() == expected_output.all()


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
