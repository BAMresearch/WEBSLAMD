from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame
from pandas.core.indexes.numeric import Int64Index
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from slamd import create_app
from slamd.common.error_handling import DatasetNotFoundException, PlotDataNotFoundException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.models.prediction import Prediction
from slamd.discovery.processing.models.tsne_plot_data import TSNEPlotData
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy
from slamd.discovery.processing.strategies.excel_strategy import ExcelStrategy
from tests.discovery.processing.test_dataframe_dicts import *

app = create_app('testing', with_session=False)


def test_save_dataset_returns_form_with_errors_when_empty():
    with app.test_request_context('/materials/discovery'):
        valid, form = DiscoveryService.save_dataset(ImmutableMultiDict(), ImmutableMultiDict())
        assert valid is False
        assert isinstance(form, UploadDatasetForm)


def test_save_dataset_saves_dataset(monkeypatch):
    headers = 'column1,column2,column3\n'
    content = '1,2,3\n4,5,6\n7,8,9'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    mock_create_dataset_called_with = None

    def mock_create_dataset(file_data):
        nonlocal mock_create_dataset_called_with
        mock_create_dataset_called_with = file_data
        return 'TestDataset.csv'

    monkeypatch.setattr(CsvStrategy, 'create_dataset', mock_create_dataset)

    mock_save_dataset_called_with = None

    def mock_save_dataset(dataset):
        nonlocal mock_save_dataset_called_with
        mock_save_dataset_called_with = dataset
        return None

    monkeypatch.setattr(CsvStrategy, 'save_dataset', mock_save_dataset)

    with app.test_request_context('/materials/discovery'):
        form = ImmutableMultiDict([('upload_button', 'Upload dataset')])
        files = ImmutableMultiDict([('dataset', file_data)])
        valid, form = DiscoveryService.save_dataset(form, files)
        assert valid is True
        assert form is None
        assert mock_create_dataset_called_with == file_data
        assert mock_save_dataset_called_with == 'TestDataset.csv'


def test_list_columns_returns_columns_of_dataset_with_given_name(monkeypatch):
    mock_query_dataset_by_name_called_with = None

    def mock_query_dataset_by_name(dataset_name):
        nonlocal mock_query_dataset_by_name_called_with
        mock_query_dataset_by_name_called_with = dataset_name
        return Dataset('test csv_strategy', dataframe=DataFrame([1, 2, 3], columns=['Index']))

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)

    columns = DiscoveryService.list_columns('test csv_strategy')
    assert mock_query_dataset_by_name_called_with == 'test csv_strategy'
    assert columns == ['Index']


def test_list_columns_raises_dataset_not_found_when_invalid_name_is_given():
    with app.test_request_context('/materials/base/invalid'):
        with pytest.raises(DatasetNotFoundException):
            DiscoveryService.list_columns('invalid csv_strategy')


def test_list_datasets_returns_empty_list_when_no_datasets(monkeypatch):
    def mock_find_all_datasets():
        return []

    monkeypatch.setattr(DiscoveryPersistence, 'find_all_datasets', mock_find_all_datasets)
    datasets = DiscoveryService.list_datasets()
    assert datasets == []


def test_list_datasets_returns_all_datasets(monkeypatch):
    def mock_find_all_datasets():
        return [
            Dataset('Dataset 1'),
            Dataset('Dataset 2'),
            Dataset('Dataset 3')
        ]

    monkeypatch.setattr(DiscoveryPersistence, 'find_all_datasets', mock_find_all_datasets)

    datasets = DiscoveryService.list_datasets()
    assert len(datasets) == 3
    assert datasets[0] == Dataset('Dataset 1')
    assert datasets[1] == Dataset('Dataset 2')
    assert datasets[2] == Dataset('Dataset 3')


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
    assert list(mock_save_tsne_plot_data_called_with.label_index.values) == [0, 1, 2, 3]
    assert list(mock_save_tsne_plot_data_called_with.nolabel_index.values) == [4, 5, 6, 7, 8, 9, 10, 11, 12]


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
    assert list(mock_save_tsne_plot_data_called_with.label_index.values) == [0, 1, 2, 3]
    assert list(mock_save_tsne_plot_data_called_with.nolabel_index.values) == [4, 5, 6, 7, 8, 9, 10, 11, 12]


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


def test_download_prediction(monkeypatch):
    def mock_query_prediction():
        return Prediction('test_dataset.csv', pd.DataFrame())

    def mock_query_dataset_by_name(dataset_name):
        if dataset_name == 'test_dataset.csv':
            return Dataset(name=dataset_name, dataframe=pd.DataFrame())
        return None

    # We do not want to test the creation of the xlsx but rather that the PredictionOutputFileGenerator is called
    def mock_create_prediction_excel(dataset, prediction):
        return 'Dummy.xslx'

    monkeypatch.setattr(DiscoveryPersistence, 'query_prediction', mock_query_prediction)
    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(ExcelStrategy, 'create_prediction_excel', mock_create_prediction_excel)

    filename, output = DiscoveryService.download_prediction()
    assert output == 'Dummy.xslx'
    assert filename.startswith('predictions-test_dataset.csv')
    assert filename.endswith('.xlsx')


def test_create_tsne_plot_raises_exception_when_no_plot_data_can_be_found(monkeypatch):
    def mock_get_session_tsne_plot_data():
        return {}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_tsne_plot_data', mock_get_session_tsne_plot_data)

    with pytest.raises(PlotDataNotFoundException):
        DiscoveryService.create_tsne_plot()


def test_create_tsne_plot_calls_generator_with_proper_data(monkeypatch):
    def mock_get_session_tsne_plot_data():
        utility = pd.Series((0, 1), (1, 2))
        features_df = pd.DataFrame([1, 2])
        label_index = Int64Index([1], dtype='int64')
        nolabel_index = Int64Index([0, 1], dtype='int64')
        return TSNEPlotData(utility=utility,
                            features_df=features_df,
                            label_index=label_index,
                            nolabel_index=nolabel_index)

    mock_create_tsne_input_space_plot_called_with = None

    def mock_create_tsne_input_space_plot(plot_df):
        nonlocal mock_create_tsne_input_space_plot_called_with
        mock_create_tsne_input_space_plot_called_with = plot_df

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_tsne_plot_data', mock_get_session_tsne_plot_data)
    monkeypatch.setattr(PlotGenerator, 'create_tsne_input_space_plot', mock_create_tsne_input_space_plot)

    DiscoveryService.create_tsne_plot()

    assert mock_create_tsne_input_space_plot_called_with.to_dict() == {'Row number': {1: 1, 0: 2},
                                                                       0: {1: 0.7071067811865475,
                                                                           0: -0.7071067811865475},
                                                                       'is_train_data': {1: 'Labelled', 0: 'Predicted'},
                                                                       'Utility': {1: 1, 0: 0}}


def _mock_dataset_and_plot(monkeypatch, data, target_name):
    def mock_query_dataset_by_name(dataset_name):
        test_df = pd.DataFrame.from_dict(data)
        return Dataset('test_data', [target_name], test_df)

    # We do not want to test the creation of the actual plot but rather that the PlotGenerator is called
    def mock_create_target_scatter_plot(targets):
        return 'Dummy Plot'

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(PlotGenerator, 'create_target_scatter_plot', mock_create_target_scatter_plot)
