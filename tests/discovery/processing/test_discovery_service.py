import numpy as np
import pandas as pd
import pytest
from io import BytesIO
from pandas import DataFrame
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from slamd import create_app
from slamd.common.error_handling import DatasetNotFoundException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy
from tests.discovery.processing.test_dataframe_dicts import TEST_DF_DICT, TEST_PRED_DF_DICT

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


def test_run_experiment(monkeypatch):
    def mock_query_dataset_by_name(dataset_name):
        test_df = pd.DataFrame.from_dict(TEST_DF_DICT)
        return Dataset('test_data', test_df)

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)

    test_experiment_config = {
        'materials_data_input': ['Powder (kg)', 'Liquid (kg)', 'Aggregates (kg)', 'Custom (kg)', 'Materials', 'Prop 1',
                                 'X', 'Y', 'fe3_o2', 'al2_o3', 'ca_o', 'mg_o', 'k2_o', 's_o3', 'ti_o2', 'p2_o5', 'sr_o',
                                 'mn2_o3', 'fine', 'fine_aggregates', 'coarse_aggregates', 'water_absorption',
                                 'duration', 'temperature', 'relative humidity', 'total costs / ton',
                                 'total delivery_time '], 'target_properties': ['Target: X'],
        'a_priori_information': ['total co2_footprint / ton'],
        'model': 'Statistics-based model (Gaussian Process Regression)', 'curiosity': '1.48450244698206',
        'target_configurations': [{'max_or_min': 'max', 'weight': '1.00'}],
        'a_priori_information_configurations': [{'max_or_min': 'min', 'weight': '2.00'}]}

    df_with_prediction = DiscoveryService.run_experiment('test_data', test_experiment_config)
    assert df_with_prediction.replace({np.nan: None}).to_dict() == TEST_PRED_DF_DICT
