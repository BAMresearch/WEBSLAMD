from werkzeug.datastructures import CombinedMultiDict

from slamd.common.error_handling import DatasetNotFoundException
from slamd.common.slamd_utils import empty
from slamd.discovery.processing.add_targets_dto import AddTargetsDto
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.forms.discovery_configuration_form import DiscoveryConfigurationForm
from slamd.discovery.processing.models.dataset import Dataset
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
        all_datasets = DiscoveryPersistence.find_all_datasets()
        return list(filter(lambda dataset: dataset.name != 'temporary.csv', all_datasets))

    @classmethod
    def create_discovery_configuration_form(cls, target_names):
        form = DiscoveryConfigurationForm()
        for name in target_names:
            # Default target weight is always 1.0
            form.target_configurations.append_entry(data={'weight': 1.0})
            # Add an extra property which is not a Field containing the target name
            form.target_configurations.entries[-1].name = name
        return form

    @classmethod
    def show_dataset_for_adding_targets(cls, dataset):
        dataframe = DiscoveryPersistence.query_dataset_by_name(dataset).dataframe

        return cls._create_data_tables(dataframe)

    @classmethod
    def _create_all_dtos(cls, dataframe):
        if dataframe is None:
            return []
        columns = dataframe.columns
        target_names = list(dataframe.loc[:, columns.str.startswith('Target')])
        all_dtos = []
        preview = ''
        for i in range(len(dataframe.index)):
            for column, value in zip(columns, dataframe.iloc[i]):
                preview += f'{column}:{value}, '
            preview = preview.strip()[:-1]
            dto = AddTargetsDto(index=i, preview_of_data=preview, targets=target_names)
            preview = ''
            all_dtos.append(dto)
        return all_dtos

    @classmethod
    def add_target_name(cls, dataset, target_name):
        dataframe = None
        initial_dataset = DiscoveryPersistence.query_dataset_by_name(dataset)
        if initial_dataset:
            dataframe = initial_dataset.dataframe
        dataframe[f'Target: {target_name}'] = None

        dataset_with_new_target = Dataset(dataset, dataframe)
        DiscoveryPersistence.save_dataset(dataset_with_new_target)

        return cls._create_data_tables(dataframe)

    @classmethod
    def save_targets(cls, dataset_name, form):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        dataframe = dataset.dataframe
        all_columns = dataset.columns

        targets_column_names = list(filter(lambda column_name: column_name.startswith('Target: '), all_columns))
        for key, value in form.items():
            if key.startswith('target'):
                pieces_of_target_key = key.split('-')
                row_index = int(pieces_of_target_key[1]) - 1
                target_number_index = int(pieces_of_target_key[2]) - 1
                dataframe.at[row_index, targets_column_names[target_number_index]] = value

        DiscoveryPersistence.save_dataset(Dataset(dataset_name, dataframe))

        return cls._create_data_tables(dataframe)

    @classmethod
    def _create_data_tables(cls, dataframe):
        all_dtos = cls._create_all_dtos(dataframe)
        target_list = []
        if dataframe is not None:
            target_list = list(dataframe.loc[:, dataframe.columns.str.startswith('Target')])
        return dataframe, all_dtos, target_list
