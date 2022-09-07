import math
from dataclasses import dataclass

import numpy as np
from pandas import DataFrame

from slamd.common.error_handling import DatasetNotFoundException, ValueNotSupportedException
from slamd.common.slamd_utils import empty, not_numeric, not_empty, float_if_not_empty
from slamd.discovery.processing.add_targets_dto import TargetDto, DataWithTargetsDto
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.targets_form import TargetsForm
from slamd.discovery.processing.models.dataset import Dataset


class TargetsService:

    @classmethod
    def get_data_for_target_page(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')

        return cls._create_target_page_data(dataset)

    @classmethod
    def add_target_name(cls, dataset, target_name):
        dataframe = None
        initial_dataset = DiscoveryPersistence.query_dataset_by_name(dataset)
        if empty(initial_dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        if initial_dataset:
            dataframe = initial_dataset.dataframe
        dataframe[f'Target: {target_name}'] = np.nan

        dataset_with_new_target = Dataset(dataset, dataframe)
        DiscoveryPersistence.save_dataset(dataset_with_new_target)

        return cls._create_target_page_data(dataset_with_new_target)

    @classmethod
    def save_targets(cls, dataset_name, form):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        dataframe = dataset.dataframe
        all_columns = dataset.columns

        targets_column_names = list(filter(lambda column_name: column_name.startswith('Target: '), all_columns))
        for key, value in form.items():
            if key.startswith('target'):
                if not_empty(value) and not_numeric(value):
                    raise ValueNotSupportedException('Targets must be numeric')
                pieces_of_target_key = key.split('-')
                row_index = int(pieces_of_target_key[1]) - 1
                target_number_index = int(pieces_of_target_key[2]) - 1
                dataframe.at[row_index, targets_column_names[target_number_index]] = float_if_not_empty(value)

        updated_dataset = Dataset(dataset_name, dataframe)
        DiscoveryPersistence.save_dataset(updated_dataset)

        return cls._create_target_page_data(updated_dataset)

    @classmethod
    def _create_target_page_data(cls, dataset):
        dataframe = dataset.dataframe

        targets_form = TargetsForm()
        targets_form.choose_target_field.choices = dataset.columns

        all_dtos = cls._create_all_dtos(dataframe)
        target_name_list = []
        if dataframe is not None:
            target_name_list = list(dataframe.loc[:, dataframe.columns.str.startswith('Target')])
        return TargetPageData(dataframe, all_dtos, target_name_list, targets_form)

    @classmethod
    def _create_all_dtos(cls, dataframe):
        if dataframe is None:
            return []
        columns = dataframe.columns
        all_data_row_dtos = []
        target_dtos = []
        preview = ''
        target_list = list(dataframe.loc[:, dataframe.columns.str.startswith('Target')])
        for i in range(len(dataframe.index)):
            for column, value in zip(columns, dataframe.iloc[i]):
                preview += f'{column}:{value}, '
            preview = preview.strip()[:-1]
            for target_name in target_list:
                target_value = dataframe.at[i, target_name]
                target_value = float_if_not_empty(target_value)
                if math.isnan(target_value):
                    target_value = None
                target_dto = TargetDto(i, target_name, target_value)
                target_dtos.append(target_dto)
            dto = DataWithTargetsDto(index=i, preview_of_data=preview, targets=target_dtos)
            preview = ''
            target_dtos = []
            all_data_row_dtos.append(dto)
        return all_data_row_dtos


@dataclass
class TargetPageData:

    dataframe: DataFrame = None
    all_dtos: list[DataWithTargetsDto] = None
    target_name_list: list[str] = None
    targets_form: TargetsForm = None
