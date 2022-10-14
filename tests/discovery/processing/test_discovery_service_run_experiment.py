import numpy as np
import pandas as pd

from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from slamd.discovery.processing.models.dataset import Dataset
from tests.discovery.processing.test_dataframe_dicts import *


def test_run_experiment_with_gauss_without_thresholds_and_saves_result(monkeypatch):
    mock_save_prediction_called_with = None

    def mock_save_prediction(prediction):
        nonlocal mock_save_prediction_called_with
        mock_save_prediction_called_with = prediction
        return None

    mock_save_tsne_plot_data_called_with = None

    def mock_save_tsne_plot_data(tsne_plot_data):
        nonlocal mock_save_tsne_plot_data_called_with
        mock_save_tsne_plot_data_called_with = tsne_plot_data
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    monkeypatch.setattr(DiscoveryPersistence, 'save_tsne_plot_data', mock_save_tsne_plot_data)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITHOUT_THRESH_INPUT, 'Target: X')

    df_with_prediction, scatter_plot = DiscoveryService.run_experiment('test_data', TEST_GAUSS_WITHOUT_THRESH_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITHOUT_THRESH_PRED
    assert mock_save_prediction_called_with.dataset_used_for_prediction == 'test_data'
    assert mock_save_prediction_called_with.metadata == TEST_GAUSS_WITHOUT_THRESH_CONFIG
    assert mock_save_prediction_called_with.dataframe.replace(
        {np.nan: None}).to_dict() == TEST_GAUSS_WITHOUT_THRESH_PRED
    assert scatter_plot == 'Dummy Plot'

    assert mock_save_tsne_plot_data_called_with.utility.replace({np.nan: None}).to_dict() == TEST_GAUSS_TSNE_PLOT_UTILITY
    assert mock_save_tsne_plot_data_called_with.features_df.replace(
        {np.nan: None}).to_dict() == TEST_TSNE_PLOT_FEATURES_INDEX
    assert list(mock_save_tsne_plot_data_called_with.index_all_labelled.values) == [0, 1, 2, 3]
    assert list(mock_save_tsne_plot_data_called_with.index_none_labelled.values) == [4, 5, 6, 7, 8, 9, 10, 11, 12]


def test_run_experiment_with_random_forest_without_thresholds_and_saves_result(monkeypatch):
    mock_save_prediction_called_with = None

    def mock_save_prediction(prediction):
        nonlocal mock_save_prediction_called_with
        mock_save_prediction_called_with = prediction
        return None

    mock_save_tsne_plot_data_called_with = None

    def mock_save_tsne_plot_data(tsne_plot_data):
        nonlocal mock_save_tsne_plot_data_called_with
        mock_save_tsne_plot_data_called_with = tsne_plot_data
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    monkeypatch.setattr(DiscoveryPersistence, 'save_tsne_plot_data', mock_save_tsne_plot_data)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITHOUT_THRESH_INPUT, 'Target: X')

    df_with_prediction, scatter_plot = DiscoveryService.run_experiment('test_data', TEST_RF_WITHOUT_THRESH_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_RF_WITHOUT_THRESH_PRED
    assert mock_save_prediction_called_with.dataset_used_for_prediction == 'test_data'
    assert mock_save_prediction_called_with.metadata == TEST_RF_WITHOUT_THRESH_CONFIG
    assert mock_save_prediction_called_with.dataframe.replace(
        {np.nan: None}).to_dict() == TEST_RF_WITHOUT_THRESH_PRED
    assert scatter_plot == 'Dummy Plot'

    assert mock_save_tsne_plot_data_called_with.utility.replace({np.nan: None}).to_dict() == TEST_RF_TSNE_PLOT_UTILITY
    assert mock_save_tsne_plot_data_called_with.features_df.replace(
        {np.nan: None}).to_dict() == TEST_TSNE_PLOT_FEATURES_INDEX
    assert list(mock_save_tsne_plot_data_called_with.index_all_labelled.values) == [0, 1, 2, 3]
    assert list(mock_save_tsne_plot_data_called_with.index_none_labelled.values) == [4, 5, 6, 7, 8, 9, 10, 11, 12]


# Since we already check for the data of the tsne plot generation in the tests above,
# we restrict this test to the experiment data itself and only make sure that the tsne plot save method was called
def test_run_experiment_with_thresholds_and_gauss_and_saves_result(monkeypatch):
    mock_save_prediction_called_with = None

    def mock_save_prediction(prediction):
        nonlocal mock_save_prediction_called_with
        mock_save_prediction_called_with = prediction
        return None

    mock_save_tsne_plot_data_called_with = None

    def mock_save_tsne_plot_data(tsne_plot_data):
        nonlocal mock_save_tsne_plot_data_called_with
        mock_save_tsne_plot_data_called_with = "Saving TSNE Plot Data"
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    monkeypatch.setattr(DiscoveryPersistence, 'save_tsne_plot_data', mock_save_tsne_plot_data)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITH_THRESH_INPUT, 'X')

    df_with_prediction, scatter_plot = DiscoveryService.run_experiment('test_data', TEST_GAUSS_WITH_THRESH_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITH_THRESH_PRED
    assert mock_save_prediction_called_with.dataset_used_for_prediction == 'test_data'
    assert mock_save_prediction_called_with.metadata == TEST_GAUSS_WITH_THRESH_CONFIG
    assert mock_save_prediction_called_with.dataframe.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITH_THRESH_PRED
    assert scatter_plot == 'Dummy Plot'
    assert mock_save_tsne_plot_data_called_with == 'Saving TSNE Plot Data'


def test_run_experiment_with_partially_labelled_data(monkeypatch):
    mock_save_prediction_called_with = None

    def mock_save_prediction(prediction):
        nonlocal mock_save_prediction_called_with
        mock_save_prediction_called_with = prediction
        return None

    def mock_save_tsne_plot_data(tsne_plot_data):
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    monkeypatch.setattr(DiscoveryPersistence, 'save_tsne_plot_data', mock_save_tsne_plot_data)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITH_PART_LABELS_INPUT, ['targ1', 'targ2'])

    df_with_prediction, scatter_plot = DiscoveryService.run_experiment('test_data', TEST_GAUSS_WITH_PART_LABELS_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITH_PART_LABELS_PRED
    assert mock_save_prediction_called_with.metadata == TEST_GAUSS_WITH_PART_LABELS_CONFIG


def _mock_dataset_and_plot(monkeypatch, data, target_names):
    def mock_query_dataset_by_name(dataset_name):
        test_df = pd.DataFrame.from_dict(data)
        if type(target_names) == str:
            return Dataset('test_data', [target_names], test_df)
        else:
            return Dataset('test_data', target_names, test_df)

    # We do not want to test the creation of the actual plot but rather that the PlotGenerator is called
    def mock_create_target_scatter_plot(targets):
        return 'Dummy Plot'

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(PlotGenerator, 'create_target_scatter_plot', mock_create_target_scatter_plot)
