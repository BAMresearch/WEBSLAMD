import numpy as np
import pandas as pd
from werkzeug.datastructures import ImmutableMultiDict

from slamd import create_app
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.targets_service import TargetsService

app = create_app('testing', with_session=False)


def test_add_target(monkeypatch):
    _mock_discovery_persistence(monkeypatch)

    with app.test_request_context('/materials/discovery'):
        target_page_data = TargetsService.add_target_name('test_data.csv', 'X')
    dtos = target_page_data.all_dtos

    assert target_page_data.dataframe.replace({np.nan: None}).to_dict() == {'feature1': {0: 1},
                                                                            'Test Target': {0: 2},
                                                                            'X': {0: None}}
    assert target_page_data.target_name_list == ['Test Target', 'X']
    assert target_page_data.targets_form.choose_target_field.choices == ['feature1', 'Test Target', 'X']
    assert len(dtos) == 1
    assert dtos[0].index == 0
    assert dtos[0].preview_of_data == 'feature1: 1.0, Test Target: 2.0, X: nan'
    assert len(dtos[0].targets) == 2
    assert dtos[0].targets[0].index == 0
    assert dtos[0].targets[0].name == 'Test Target'
    assert dtos[0].targets[0].value == 2
    assert dtos[0].targets[1].index == 0
    assert dtos[0].targets[1].name == 'X'
    assert dtos[0].targets[1].value is None


def test_save_targets(monkeypatch):
    _mock_discovery_persistence(monkeypatch)

    form = ImmutableMultiDict([('target-1-1', '11.2'), ('submit', '3 - Save targets')])
    with app.test_request_context('/materials/discovery'):
        target_page_data = TargetsService.save_targets('test_data', form)

    dtos = target_page_data.all_dtos

    assert target_page_data.dataframe.to_dict() == {'feature1': {0: 1}, 'Test Target': {0: 11.2}}
    assert target_page_data.target_name_list == ['Test Target']
    assert len(dtos) == 1
    assert dtos[0].index == 0
    assert dtos[0].preview_of_data == 'feature1: 1.0, Test Target: 11.2'
    assert len(dtos[0].targets) == 1
    assert dtos[0].targets[0].index == 0
    assert dtos[0].targets[0].name == 'Test Target'
    assert dtos[0].targets[0].value == 11.2


def test_toggle_targets_for_editing_scenario_disabling(monkeypatch):
    _mock_discovery_persistence(monkeypatch)

    with app.test_request_context('/materials/discovery'):
        target_page_data = TargetsService.toggle_targets_for_editing('test_data', ['Test Target'])

    dtos = target_page_data.all_dtos

    assert target_page_data.target_name_list == []
    assert len(dtos) == 1
    assert dtos[0].index == 0
    assert dtos[0].preview_of_data == 'feature1: 1, Test Target: 2'
    assert len(dtos[0].targets) == 0


def test_toggle_targets_for_editing_scenario_enabling(monkeypatch):
    def mock_query_dataset_by_name(dataset_name):
        test_df = {'feature1': [1], 'Test Target': [2]}
        dataframe = pd.DataFrame.from_dict(test_df)
        return Dataset(name=dataset_name, dataframe=dataframe)

    def mock_save_dataset(dataset):
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', mock_save_dataset)

    with app.test_request_context('/materials/discovery'):
        target_page_data = TargetsService.toggle_targets_for_editing('test_data', ['Test Target'])

    dtos = target_page_data.all_dtos

    assert target_page_data.target_name_list == ['Test Target']
    assert len(dtos) == 1
    assert dtos[0].index == 0
    assert dtos[0].preview_of_data == 'feature1: 1, Test Target: 2'
    assert len(dtos[0].targets) == 1
    assert dtos[0].targets[0].index == 0
    assert dtos[0].targets[0].name == 'Test Target'
    assert dtos[0].targets[0].value == 2


def _mock_discovery_persistence(monkeypatch):
    def mock_query_dataset_by_name(dataset_name):
        test_df = {'feature1': [1], 'Test Target': [2]}
        dataframe = pd.DataFrame.from_dict(test_df)
        return Dataset(dataset_name, ['Test Target'], dataframe)

    def mock_save_dataset(dataset):
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', mock_save_dataset)
