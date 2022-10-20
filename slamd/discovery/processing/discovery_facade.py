from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence

TEMPORARY_CONCRETE_FORMULATION = 'temporary_concrete.csv'
TEMPORARY_BINDER_FORMULATION = 'temporary_binder.csv'


class DiscoveryFacade:

    @classmethod
    def save_dataset(cls, dataset):
        DiscoveryPersistence.save_dataset(dataset)

    @classmethod
    def delete_dataset_by_name(cls, dataset_name):
        return DiscoveryPersistence.delete_dataset_by_name(dataset_name)

    @classmethod
    def query_dataset_by_name(cls, dataset_name):
        return DiscoveryPersistence.query_dataset_by_name(dataset_name)

    @classmethod
    def find_all_datasets(cls):
        return DiscoveryPersistence.find_all_datasets()

    @classmethod
    def save_and_overwrite_dataset(cls, dataset, filename):
        DiscoveryFacade.delete_dataset_by_name(filename)
        DiscoveryFacade.save_dataset(dataset)
