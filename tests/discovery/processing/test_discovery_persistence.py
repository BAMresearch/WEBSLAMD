from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset


def test_save_dataset_sets_new_dataset(monkeypatch):
    def mock_get_session_property():
        return {}

    mock_set_session_property_called_with = None

    def mock_set_session_property(datasets):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = datasets
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)
    monkeypatch.setattr(DiscoveryPersistence, 'set_session_property', mock_set_session_property)

    dataset = Dataset(name='test name')
    DiscoveryPersistence.save_dataset(dataset)
    assert mock_set_session_property_called_with == {dataset.name: dataset}


def test_save_dataset_appends_dataset_to_existing_ones(monkeypatch):
    def mock_get_session_property():
        return [Dataset('test dataset')]

    mock_extend_session_property_called_with = None

    def mock_extend_session_property(dataset):
        nonlocal mock_extend_session_property_called_with
        mock_extend_session_property_called_with = dataset
        return None

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)
    monkeypatch.setattr(DiscoveryPersistence, 'extend_session_property', mock_extend_session_property)

    dataset = Dataset(name='test new dataset')
    DiscoveryPersistence.save_dataset(dataset)
    assert mock_extend_session_property_called_with == dataset


def test_delete_dataset_by_name_removes_dataset_of_specified_name(monkeypatch):
    to_be_removed = Dataset('to be removed')
    to_be_kept = Dataset('to be kept')

    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {'to be removed': to_be_removed, 'to be kept': to_be_kept}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    deleted_dataset = DiscoveryPersistence.delete_dataset_by_name('to be removed')
    assert mock_get_session_property_called is True
    assert deleted_dataset == to_be_removed


def test_query_dataset_by_name_calls_session(monkeypatch):
    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {'test dataset': Dataset('test dataset')}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)
    result = DiscoveryPersistence.query_dataset_by_name('test dataset')

    assert result == Dataset('test dataset')
    assert mock_get_session_property_called is True


def test_query_dataset_by_name_returns_dataset_of_specified_name(monkeypatch):
    to_be_returned = Dataset('to be returned')

    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {'to be returned': to_be_returned, 'another dataset': Dataset('another dataset')}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.query_dataset_by_name('to be returned')
    assert result == to_be_returned
    assert mock_get_session_property_called is True


def test_query_dataset_by_name_returns_none_if_not_found(monkeypatch):
    to_be_returned = Dataset('to be returned')

    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {'to be returned': to_be_returned, 'another dataset': Dataset('another dataset')}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.query_dataset_by_name('not found')
    assert result is None
    assert mock_get_session_property_called is True


def test_find_all_datasets_returns_empty_list_at_start(monkeypatch):
    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.find_all_datasets()
    assert len(result) == 0
    assert result == []
    assert mock_get_session_property_called is True


def test_find_all_datasets_returns_datasets_as_list(monkeypatch):
    mock_get_session_property_called = False

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return {'dataset 1': Dataset('dataset 1'), 'dataset 2': Dataset('dataset 2')}

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.find_all_datasets()
    assert len(result) == 2
    assert result == [Dataset('dataset 1'), Dataset('dataset 2')]
    assert mock_get_session_property_called is True
