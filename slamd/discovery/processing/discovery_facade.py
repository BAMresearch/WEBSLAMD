from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence

TEMPORARY_FORMULATION = 'temporary.csv'


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
    def save_temporary_dataset(cls, dataset):
        DiscoveryFacade.delete_dataset_by_name(TEMPORARY_FORMULATION)
        DiscoveryFacade.save_dataset(dataset)
