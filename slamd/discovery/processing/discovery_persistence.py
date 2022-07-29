from flask import session


class DiscoveryPersistence:

    @classmethod
    def save_dataset(cls, dataset):
        cls.extend_session_property(dataset)

    @classmethod
    def delete_dataset_by_name(cls, dataset_name):
        datasets = cls.get_session_property()
        return datasets.pop(dataset_name, None)

    @classmethod
    def query_dataset_by_name(cls, dataset_name):
        """
        Return the first element matching the given dataset name.
        Return None if no matching element was found.
        """
        datasets = cls.get_session_property()
        return datasets.get(dataset_name, None)

    @classmethod
    def find_all_datasets(cls):
        datasets = cls.get_session_property()
        return list(datasets.values())

    """
    Wrappers for session logic. This way we can easily mock the methods in tests without any need for creating a proper
    context and session. Check test_discovery_persistence for examples.
    """
    @classmethod
    def get_session_property(cls):
        return session.get('datasets', {})

    @classmethod
    def extend_session_property(cls, dataset):
        datasets = cls.get_session_property()
        datasets[dataset.name] = dataset
