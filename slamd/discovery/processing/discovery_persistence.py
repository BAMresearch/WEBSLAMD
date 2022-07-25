from flask import session


class DiscoveryPersistence:

    @classmethod
    def save_dataset(cls, dataset):
        before = cls.get_session_property()

        if not before:
            cls.set_session_property([dataset])
        else:
            cls.extend_session_property(dataset)

    @classmethod
    def delete_dataset_by_name(cls, dataset_name):
        datasets = cls.get_session_property()
        remaining_datasets = list(filter(lambda ds: ds.name != dataset_name, datasets))
        cls.set_session_property(remaining_datasets)

    @classmethod
    def query_dataset_by_name(cls, dataset_name):
        """
        Return the first element matching the given dataset name.
        Return None if no matching element was found.
        """
        datasets = cls.get_session_property()
        for ds in datasets:
            if ds.name == dataset_name:
                return ds
        # Nothing found
        return None

    """
    Wrappers for session logic. This way we can easily mock the methods in tests without any need for creating a proper
    context and session. Check test_discovery_persistence for examples.
    """
    @classmethod
    def get_session_property(cls):
        return session.get('datasets', [])

    @classmethod
    def set_session_property(cls, datasets):
        session['datasets'] = datasets

    @classmethod
    def extend_session_property(cls, dataset):
        session['datasets'].append(dataset)
