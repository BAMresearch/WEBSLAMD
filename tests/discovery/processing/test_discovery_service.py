from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from slamd import create_app
from slamd.common.error_handling import DatasetNotFoundException
from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from slamd.discovery.processing.strategies.excel_strategy import ExcelStrategy
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.models.prediction import Prediction
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy
from tests.discovery.processing.test_dataframe_dicts import TEST_GAUSS_WITHOUT_THRESH_INPUT, \
    TEST_GAUSS_WITH_THRESH_INPUT, TEST_GAUSS_WITHOUT_THRESH_PRED, \
    TEST_GAUSS_WITH_THRESH_PRED, TEST_GAUSS_WITHOUT_THRESH_CONFIG, TEST_GAUSS_WITH_THRESH_CONFIG

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

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITHOUT_THRESH_INPUT, 'Target: X')

    df_with_prediction, scatter_plot, tsne_plot = DiscoveryService.run_experiment(
        'test_data', TEST_GAUSS_WITHOUT_THRESH_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITHOUT_THRESH_PRED
    assert mock_save_prediction_called_with.dataset_used_for_prediction == 'test_data'
    assert mock_save_prediction_called_with.metadata == TEST_GAUSS_WITHOUT_THRESH_CONFIG
    assert mock_save_prediction_called_with.dataframe.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITHOUT_THRESH_PRED
    assert scatter_plot == 'Dummy Plot'
    assert tsne_plot == 'Dummy Plot'


def test_run_experiment_with_thresholds_and_gauss_and_saves_result(monkeypatch):
    mock_save_prediction_called_with = None

    def mock_save_prediction(prediction):
        nonlocal mock_save_prediction_called_with
        mock_save_prediction_called_with = prediction
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_prediction', mock_save_prediction)
    _mock_dataset_and_plot(monkeypatch, TEST_GAUSS_WITH_THRESH_INPUT, 'X')

    df_with_prediction, scatter_plot, tsne_plot = DiscoveryService.run_experiment(
        'test_data', TEST_GAUSS_WITH_THRESH_CONFIG)

    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITH_THRESH_PRED
    assert mock_save_prediction_called_with.dataset_used_for_prediction == 'test_data'
    assert mock_save_prediction_called_with.metadata == TEST_GAUSS_WITH_THRESH_CONFIG
    assert mock_save_prediction_called_with.dataframe.replace({np.nan: None}).to_dict() == TEST_GAUSS_WITH_THRESH_PRED
    assert scatter_plot == 'Dummy Plot'
    assert tsne_plot == 'Dummy Plot'


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


def _mock_dataset_and_plot(monkeypatch, data, target_name):
    def mock_query_dataset_by_name(dataset_name):
        test_df = pd.DataFrame.from_dict(data)
        return Dataset('test_data', [target_name], test_df)

    # We do not want to test the creation of the actual plot but rather that the PlotGenerator is called
    def mock_create_target_scatter_plot(targets):
        return 'Dummy Plot'

     # We do not want to test the creation of the actual plot but rather that the PlotGenerator is called
    def mock_create_tsne_input_space_plot(features):
        return 'Dummy Plot'

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(PlotGenerator, 'create_target_scatter_plot', mock_create_target_scatter_plot)
    monkeypatch.setattr(PlotGenerator, 'create_tsne_input_space_plot', mock_create_tsne_input_space_plot)
