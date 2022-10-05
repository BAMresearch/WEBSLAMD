from io import BytesIO
from werkzeug.datastructures import FileStorage

from slamd.common.error_handling import SlamdUnprocessableEntityException, SlamdRequestTooLargeException, \
    ValueNotSupportedException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy

import pytest


def test_create_dataset_parses_file_storage_correctly(monkeypatch):
    headers = 'column1,column2,column3\n'
    content = '1,2,3\n4,5,6\n7,8,9'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)
    dataset = CsvStrategy.create_dataset(file_data)
    assert dataset.name == 'TestDataset.csv'
    assert len(dataset.columns) == 3
    for col in zip(dataset.columns, ['column1', 'column2', 'column3']):
        assert col[0] == col[1]
    assert dataset.dataframe.iloc[0].tolist() == [1, 2, 3]
    assert dataset.dataframe.iloc[1].tolist() == [4, 5, 6]
    assert dataset.dataframe.iloc[2].tolist() == [7, 8, 9]


def test_create_dataset_filename_error(monkeypatch):
    headers = 'column1,column2,column3\n'
    content = '1,2,3\n4,5,6\n7,8,9'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='temporary.csv', stream=stream)

    with pytest.raises(ValueNotSupportedException):
        CsvStrategy.create_dataset(file_data)


def test_create_dataset_parsing_error(monkeypatch):
    headers = 'column1,column2,column3\n'
    content = '1,2,3\n,6\n7,,,,'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    with pytest.raises(SlamdUnprocessableEntityException):
        CsvStrategy.create_dataset(file_data)


def test_create_dataset_string_parsing():
    headers = 'column1,column2,column3\n'
    content = '"1","2",3\n"4","5",6\n"7","b",9'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    dataset = CsvStrategy.create_dataset(file_data)

    assert dataset.dataframe['column1'].tolist() == [1, 4, 7]
    assert dataset.dataframe['column2'].tolist() == ['2', '5', 'b']
    assert dataset.dataframe['column3'].tolist() == [3, 6, 9]


def test_save_dataset_calls_discovery_persistence(monkeypatch):
    mock_save_dataset_called_with = None

    def mock_save_dataset(dataset):
        nonlocal mock_save_dataset_called_with
        mock_save_dataset_called_with = dataset
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', mock_save_dataset)

    dataset = Dataset(name='TestDataset.csv')
    CsvStrategy.save_dataset(dataset)
    assert mock_save_dataset_called_with == dataset


def test_delimiter_parsing_semicolon():
    headers = 'column1;column2;column3\n'
    content = '1,1;2,1;3,4\n4,2;5,7;6,0\n7,3;8;9,7'
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    assert CsvStrategy._determine_delimiter(file_data) == ';'


def test_delimiter_parsing_excessive_columns():
    headers = ','.join([f'column{i}' for i in range(10000)])
    row = ','.join([f'{i}' for i in range(10000)])
    content = '\n'.join([row] * 3)

    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    with pytest.raises(SlamdRequestTooLargeException):
        CsvStrategy._determine_delimiter(file_data)


def test_delimiter_parsing_insufficient_rows():
    headers = 'column1,column2,column3\n'
    content = ''
    stream = BytesIO(bytes(headers + content, 'utf-8'))
    file_data = FileStorage(filename='TestDataset.csv', stream=stream)

    with pytest.raises(SlamdUnprocessableEntityException):
        CsvStrategy._determine_delimiter(file_data)
