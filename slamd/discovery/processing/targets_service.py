import math

import numpy as np

from slamd.common.error_handling import DatasetNotFoundException, ValueNotSupportedException
from slamd.common.slamd_utils import empty, not_numeric, not_empty, float_if_not_empty
from slamd.discovery.processing.add_targets_dto import TargetDto, DataWithTargetsDto
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.targets_form import TargetsForm
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.target_page_data import TargetPageData


class TargetsService:

    @classmethod
    def get_data_for_target_page(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')

        return cls._create_target_page_data(dataset)

    @classmethod
    def add_target_name(cls, dataset, target_name):
        if empty(target_name):
            raise ValueNotSupportedException('Target name cannot be empty')

        initial_dataset = DiscoveryPersistence.query_dataset_by_name(dataset)
        if empty(initial_dataset):
            raise DatasetNotFoundException('Dataset with given name not found')

        dataframe = initial_dataset.dataframe

        if target_name in initial_dataset.columns:
            raise ValueNotSupportedException('The chosen target name already exists in the dataset')

        dataframe[target_name] = np.nan
        initial_dataset.target_columns.append(target_name)

        dataset_with_new_target = Dataset(dataset, initial_dataset.target_columns, dataframe)
        DiscoveryPersistence.save_dataset(dataset_with_new_target)

        return cls._create_target_page_data(dataset_with_new_target)

    @classmethod
    def save_targets(cls, dataset_name, form):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        dataframe = dataset.dataframe

        for key, value in form.items():
            if key.startswith('target'):
                if not_empty(value) and not_numeric(value):
                    raise ValueNotSupportedException('Targets must be numeric')
                pieces_of_target_key = key.split('-')
                row_index = int(pieces_of_target_key[1]) - 1
                target_number_index = int(pieces_of_target_key[2]) - 1
                dataframe.at[row_index, dataset.target_columns[target_number_index]] = float_if_not_empty(value)

        updated_dataset = Dataset(dataset_name, dataset.target_columns, dataframe)
        DiscoveryPersistence.save_dataset(updated_dataset)

        return cls._create_target_page_data(updated_dataset)

    @classmethod
    def _create_target_page_data(cls, dataset):
        dataframe = dataset.dataframe

        targets_form = TargetsForm()
        targets_form.choose_target_field.choices = dataset.columns

        all_dtos = cls._create_all_dtos(dataset)
        return TargetPageData(dataframe, all_dtos, dataset.target_columns, targets_form)

    @classmethod
    def _create_all_dtos(cls, dataset):
        if dataset.dataframe is None:
            return []
        columns = dataset.columns
        dataframe = dataset.dataframe
        all_data_row_dtos = []

        for i in range(len(dataframe.index)):
            preview = ''
            for column, value in zip(columns, dataframe.iloc[i]):
                preview += f'{column}: {value}, '
            preview = preview.strip()[:-1]

            target_dtos = []
            for target_name in dataset.target_columns:
                target_value = dataframe.at[i, target_name]
                target_value = float_if_not_empty(target_value)
                if math.isnan(target_value):
                    target_value = None
                target_dto = TargetDto(i, target_name, target_value)
                target_dtos.append(target_dto)

            dto = DataWithTargetsDto(index=i, preview_of_data=preview, targets=target_dtos)
            all_data_row_dtos.append(dto)

        return all_data_row_dtos

    @classmethod
    def toggle_targets_for_editing(cls, dataset_name, names_of_targets_to_be_edited):
        if len(names_of_targets_to_be_edited) == 0:
            raise ValueNotSupportedException('You must specify at least on target to be labelled')

        dataframe = None
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        if dataset:
            dataframe = dataset.dataframe

        for name in names_of_targets_to_be_edited:
            if dataframe[name].dtype == object or dataframe[name].dtype == str:
                raise ValueNotSupportedException('Only numeric columns can be edited')

            if name in dataset.target_columns:
                dataset.target_columns.remove(name)
            else:
                dataset.target_columns.append(name)

        dataset_with_new_target = Dataset(dataset_name, dataset.target_columns, dataframe)
        DiscoveryPersistence.save_dataset(dataset_with_new_target)

        return cls._create_target_page_data(dataset_with_new_target)
