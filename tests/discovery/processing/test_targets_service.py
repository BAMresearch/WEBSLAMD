from werkzeug.datastructures import ImmutableMultiDict

from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.targets_service import TargetsService


def test_save_targets(monkeypatch):
    def mock_query_dataset_by_name(dataset_name):
        test_df = {'feature1': [1], 'Target: Test Target': [2]}
        import pandas as pd
        dataframe = pd.DataFrame.from_dict(test_df)
        return Dataset(dataset_name, dataframe)

    def mock_save_dataset(dataset):
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', mock_save_dataset)

    form = ImmutableMultiDict([('target-1-1', '11.2'), ('submit', '3 - Save targets')])
    df, dtos, targets = TargetsService.save_targets('test_data', form)

    assert df.to_dict() == {'feature1': {0: 1}, 'Target: Test Target': {0: 11.2}}
    assert len(dtos) == 1
    assert dtos[0].index == 0
    assert dtos[0].preview_of_data == 'feature1:1.0, Target: Test Target:11.2'
    assert len(dtos[0].targets) == 1
    assert dtos[0].targets[0].index == 0
    assert dtos[0].targets[0].name == 'Target: Test Target'
    assert dtos[0].targets[0].value == 11.2
