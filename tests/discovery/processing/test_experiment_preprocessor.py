import numpy as np
import pandas as pd
import pytest

from slamd.common.error_handling import ValueNotSupportedException, SequentialLearningException, \
    SlamdUnprocessableEntityException
from slamd.discovery.processing.experiment.experiment_preprocessor import ExperimentPreprocessor
from slamd.discovery.processing.experiment.experiment_data import ExperimentData
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel


def create_valid_experimentdata():
    """
    Creates a valid ExperimentData object for ExperimentPreprocessor.validate_experiment() tests.
    Do not use for other tests - the Dataframes are filled with dummy data.
    """
    feature_names = ['feature1', 'feature2', 'feature3']
    target_names = ['target1', 'target2', 'target3']
    apriori_names = ['apriori1', 'apriori2', 'apriori3']

    df = pd.DataFrame(columns=feature_names + target_names + apriori_names)

    for col in feature_names+apriori_names:
        df[col] = np.arange(10)

    df.loc[1, target_names] = [1, 2, 3]
    df.loc[4, target_names] = [4, 5, 6]
    df.loc[5, target_names] = [6, 7, 8]

    return ExperimentData(
        dataframe=df,
        model=str(ExperimentModel.GAUSSIAN_PROCESS.value),
        curiosity=2,

        target_names=target_names,
        target_weights=[1, 2, 1],
        target_thresholds=[None, 5, 6],
        target_max_or_min=['max', 'max', 'min'],

        apriori_names=apriori_names,
        apriori_weights=[1, 2, 1],
        apriori_thresholds=[None, 5, 6],
        apriori_max_or_min=['max', 'max', 'min'],

        feature_names=feature_names
    )


def test_validate_experiment_valid():
    exp = create_valid_experimentdata()
    ExperimentPreprocessor.validate_experiment(exp)

    # If the experiment is valid and this point is reached, the test completes. No assert necessary.


def test_validate_experiment_invalid_model():
    exp = create_valid_experimentdata()
    exp.model = 'Invalid model name'

    with pytest.raises(ValueNotSupportedException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_validate_experiment_length_mismatch():
    exp = create_valid_experimentdata()
    exp.target_weights = exp.target_weights[:-1]

    with pytest.raises(SlamdUnprocessableEntityException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_validate_experiment_invalid_maxmin():
    exp = create_valid_experimentdata()
    exp.target_max_or_min[0] = 'Invalid value'

    with pytest.raises(SequentialLearningException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_validate_experiment_no_targets():
    exp = create_valid_experimentdata()
    exp.target_names = []
    exp.target_weights = []
    exp.target_max_or_min = []

    with pytest.raises(SequentialLearningException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_validate_experiment_no_labels_gauss():
    exp = create_valid_experimentdata()
    exp.dataframe.loc[:, ['target1', 'target2', 'target3']] = np.nan

    with pytest.raises(ValueNotSupportedException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_validate_experiment_no_labels_forest():
    exp = create_valid_experimentdata()
    exp.dataframe.loc[[4, 5], ['target1', 'target2', 'target3']] = np.nan
    exp.model = str(ExperimentModel.RANDOM_FOREST.value)

    with pytest.raises(ValueNotSupportedException):
        ExperimentPreprocessor.validate_experiment(exp)


def test_filter_apriori_thresholds():
    df = pd.DataFrame()
    df['u'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['v'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df['x'] = [np.nan, np.nan, np.nan, 4, np.nan, np.nan, 7, 8]
    df['y'] = [1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 8]

    experiment = ExperimentData(dataframe=df, target_names=['x', 'y'], apriori_names=['u', 'v'],
                                apriori_thresholds=[4, 5], apriori_max_or_min=['max', 'min'])

    ExperimentPreprocessor.filter_apriori_with_thresholds_and_update_orig_data(experiment)
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

    ExperimentPreprocessor.encode_categoricals(experiment)

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

    ExperimentPreprocessor.encode_categoricals(experiment)

    assert np.array_equal(experiment.dataframe['u'].values, input_df['u'].values)
    assert np.array_equal(experiment.dataframe['v'].values, input_df['v'].values)


def test_encode_categoricals_empty():
    input_df = pd.DataFrame()

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor.encode_categoricals(experiment)

    assert experiment.dataframe.empty


def test_filter_missing_inputs_empty():
    input_df = pd.DataFrame()

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor.filter_missing_inputs(experiment)

    assert experiment.dataframe.empty


def test_filter_missing_inputs_multiple():
    input_df = pd.DataFrame({
        'u': [1, 2, 3],
        'v': [1.0, np.nan, 4.5],
        'w': ['a', 'b', 'c'],
        'x': ['asdf', 'qwer', np.nan]
    })

    experiment = ExperimentData(
        dataframe=input_df,
        feature_names=list(input_df.columns)
    )

    ExperimentPreprocessor.filter_missing_inputs(experiment)

    assert tuple(experiment.dataframe.columns) == ('u', 'w')
