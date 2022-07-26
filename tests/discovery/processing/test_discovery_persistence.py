from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset


def test_save_dataset_sets_new_dataset(monkeypatch):
    def mock_get_session_property():
        return []

    mock_set_session_property_called_with = None

    def mock_set_session_property(datasets):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = datasets
        return None

    monkeypatch.setattr(DiscoveryPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(DiscoveryPersistence,
                        'set_session_property', mock_set_session_property)

    dataset = Dataset()
    DiscoveryPersistence.save_dataset(dataset)
    assert mock_set_session_property_called_with == [dataset]


def test_save_dataset_appends_datset_to_existing_ones(monkeypatch):
    def mock_get_session_property():
        return [Dataset('test dataset')]

    mock_extend_session_property_called_with = None

    def mock_extend_session_property(dataset):
        nonlocal mock_extend_session_property_called_with
        mock_extend_session_property_called_with = dataset
        return None

    monkeypatch.setattr(DiscoveryPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(DiscoveryPersistence,
                        'extend_session_property', mock_extend_session_property)

    dataset = Dataset()
    DiscoveryPersistence.save_dataset(dataset)
    assert mock_extend_session_property_called_with == dataset


def test_delete_dataset_by_name_removes_dataset_of_specified_name(monkeypatch):
    to_be_removed = Dataset('to be removed')
    to_be_kept = Dataset('to be kept')

    def mock_get_session_property():
        return [to_be_removed, to_be_kept]

    mock_set_session_property_called_with = None

    def mock_set_session_property(datasets):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = datasets
        return None

    monkeypatch.setattr(DiscoveryPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(DiscoveryPersistence,
                        'set_session_property', mock_set_session_property)

    DiscoveryPersistence.delete_dataset_by_name('to be removed')
    assert mock_set_session_property_called_with == [to_be_kept]


def test_query_dataset_by_name_calls_session(monkeypatch):
    mock_get_session_property_called = None

    def mock_get_session_property():
        nonlocal mock_get_session_property_called
        mock_get_session_property_called = True
        return [Dataset('test dataset')]

    monkeypatch.setattr(DiscoveryPersistence,
                        'get_session_property', mock_get_session_property)
    result = DiscoveryPersistence.query_dataset_by_name('test dataset')

    assert result == Dataset('test dataset')
    assert mock_get_session_property_called is True


def test_query_dataset_by_name_returns_dataset_of_specified_name(monkeypatch):
    to_be_returned = Dataset('to be returned')

    def mock_get_session_property():
        return [to_be_returned, Dataset('another dataset')]

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.query_dataset_by_name('to be returned')
    assert result == to_be_returned


def test_query_dataset_by_name_returns_none_if_not_found(monkeypatch):
    to_be_returned = Dataset('to be returned')

    def mock_get_session_property():
        return [to_be_returned, Dataset('another dataset')]

    monkeypatch.setattr(DiscoveryPersistence, 'get_session_property', mock_get_session_property)

    result = DiscoveryPersistence.query_dataset_by_name('not found')
    assert result is None
