from werkzeug.datastructures import CombinedMultiDict

from slamd.common.error_handling import DatasetNotFoundException
from slamd.common.slamd_utils import empty
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.forms.discovery_configuration_form import DiscoveryConfigurationForm
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy


class DiscoveryService:

    @classmethod
    def save_dataset(cls, submitted_form, submitted_file):
        form = UploadDatasetForm(CombinedMultiDict((submitted_file, submitted_form)))

        if form.validate():
            dataset = CsvStrategy.create_dataset(form.dataset.data)
            CsvStrategy.save_dataset(dataset)
            return True, None
        return False, form

    @classmethod
    def delete_dataset(cls, dataset_name):
        DiscoveryPersistence.delete_dataset_by_name(dataset_name)

    @classmethod
    def list_columns(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Material with given UUID not found')
        return dataset.columns

    @classmethod
    def list_datasets(cls):
        return DiscoveryPersistence.find_all_datasets()

    @classmethod
    def create_discovery_configuration_form(cls, target_names):
        form = DiscoveryConfigurationForm()
        for name in target_names:
            # Default target weight is always 1.0
            form.target_configurations.append_entry(data={'weight': 1.0})
            # Add an extra property which is not a Field containing the target name
            form.target_configurations.entries[-1].name = name
        return form
