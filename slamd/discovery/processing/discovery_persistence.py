from flask import session


class DiscoveryPersistence:

    @classmethod
    def save_dataset(cls, dataset):
        before = cls.get_session_property()

        if not before:
            cls.set_session_property({dataset.name: dataset})
        else:
            cls.extend_session_property(dataset)

    @classmethod
    def save_prediction(cls, prediction):
        cls.set_session_prediction(prediction)

    @classmethod
    def save_tsne_plot_data(cls, tsne_plot_data):
        cls.set_session_tsne_plot_data(tsne_plot_data)

    @classmethod
    def set_session_prediction(cls, prediction):
        session['sequential_learning_predictions'] = prediction

    @classmethod
    def set_session_tsne_plot_data(cls, tsne_plot_data):
        session['tsne_plot_data'] = tsne_plot_data

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
    def query_prediction(cls):
        """
        Return the first element matching the given dataset name.
        Return None if no matching element was found.
        """
        return cls.get_session_prediction()

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
    def get_session_prediction(cls):
        return session.get('sequential_learning_predictions', {})

    @classmethod
    def get_session_tsne_plot_data(cls):
        return session.get('tsne_plot_data', {})

    @classmethod
    def set_session_property(cls, datasets):
        session['datasets'] = datasets

    @classmethod
    def extend_session_property(cls, dataset):
        session['datasets'][dataset.name] = dataset

