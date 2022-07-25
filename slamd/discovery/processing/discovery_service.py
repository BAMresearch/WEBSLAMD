from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy
from slamd.discovery.processing.models.dataset import Dataset


class DiscoveryService:

    @classmethod
    def upload_dataset(cls, submitted_form, submitted_dataset):
        form = UploadDatasetForm(submitted_form)

        if form.validate():
            dataset = CsvStrategy.create_dataset(submitted_dataset)
            CsvStrategy.save_dataset(dataset)
            return True, None
        return False, form

    @classmethod
    def list_columns(cls, dataset):
        # Hardcoded response until we have a reliable upload button.
        return [
            'Idx_Sample',
            'SiO2',
            'CaO',
            'SO3',
            'FA (kg/m3)',
            'GGBFS (kg/m3)',
            'Coarse aggregate (kg/m3)',
            'Fine aggregate (kg/m3)',
            'Total aggregates',
            'Na2SiO3', 'Na2O (Dry)',
            'Sio2(Dry)', 'Superplasticizer',
            'water - eff', 'Slump - Target(mm)',
            'CO2(kg/t) - A-priori Information',
            'fc 28-d - Target(MPa)'
        ]

    @classmethod
    def list_datasets(cls):
        # Hardcoded answers until we have a reliable method in DatasetPersistence
        return [Dataset('My dataset 1', 'Name, Type, Cost'), Dataset('My dataset 2', 'Name, Type, Compressive Strength')]
