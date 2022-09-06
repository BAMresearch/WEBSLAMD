import math
from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd
from werkzeug.datastructures import CombinedMultiDict

from slamd.common.error_handling import DatasetNotFoundException, ValueNotSupportedException
from slamd.common.slamd_utils import empty, float_if_not_empty, not_empty, not_numeric
from slamd.discovery.processing.add_targets_dto import DataWithTargetsDto, TargetDto
from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment
from slamd.discovery.processing.algorithms.user_input import UserInput
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.discovery_form import DiscoveryForm
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.models.prediction import Prediction
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
            raise DatasetNotFoundException('Dataset with given name not found')
        return dataset.columns

    @classmethod
    def list_datasets(cls):
        all_datasets = DiscoveryPersistence.find_all_datasets()
        return list(filter(lambda dataset: dataset.name != 'temporary.csv', all_datasets))

    @classmethod
    def create_target_configuration_form(cls, target_names):
        form = DiscoveryForm()
        for name in target_names:
            form.target_configurations.append_entry()
            # Add an extra property which is not a Field containing the target name
            form.target_configurations.entries[-1].name = name
        return form

    @classmethod
    def create_a_priori_information_configuration_form(cls, a_priori_information_names):
        form = DiscoveryForm()
        for name in a_priori_information_names:
            form.a_priori_information_configurations.append_entry()
            # Add an extra property which is not a Field containing the target name
            form.a_priori_information_configurations.entries[-1].name = name
        return form

    @classmethod
    def run_experiment(cls, dataset_name, request_body):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')

        user_input = cls._parse_user_input(request_body)
        experiment = cls._initialize_experiment(dataset.dataframe, user_input)
        df_with_predictions, plot = experiment.run()

        prediction = Prediction(df_with_predictions, request_body)
        DiscoveryPersistence.save_prediction(prediction)

        return df_with_predictions, plot

    @classmethod
    def _parse_user_input(cls, discovery_form):
        target_weights = [float(conf['weight']) for conf in discovery_form['target_configurations']]
        target_max_or_min = [conf['max_or_min'] for conf in discovery_form['target_configurations']]
        fixed_target_weights = [float(conf['weight']) for conf in discovery_form['a_priori_information_configurations']]
        fixed_target_max_or_min = [conf['max_or_min'] for conf in discovery_form['a_priori_information_configurations']]

        return UserInput(
            model=discovery_form['model'],
            curiosity=float(discovery_form['curiosity']),
            features=discovery_form['materials_data_input'],
            targets=discovery_form['target_properties'],
            target_weights=target_weights,
            target_max_or_min=target_max_or_min,
            fixed_targets=discovery_form['a_priori_information'],
            fixed_target_weights=fixed_target_weights,
            fixed_target_max_or_min=fixed_target_max_or_min,
        )

    @classmethod
    def _initialize_experiment(cls, dataframe, user_input):
        return DiscoveryExperiment(
            dataframe=dataframe,
            model=user_input.model,
            curiosity=user_input.curiosity,
            features=user_input.features,
            targets=user_input.targets,
            target_weights=user_input.target_weights,
            target_max_or_min=user_input.target_max_or_min,
            fixed_targets=user_input.fixed_targets,
            fixed_target_weights=user_input.fixed_target_weights,
            fixed_target_max_or_min=user_input.fixed_target_max_or_min
        )

    @classmethod
    def download_dataset(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        # Return the CSV as a string. Represent NaNs in the dataframe as a string.
        return dataset.dataframe.to_csv(index=False, na_rep='NaN')

    @classmethod
    def download_prediction(cls):
        prediction = DiscoveryPersistence.query_prediction()
        if empty(prediction):
            raise DatasetNotFoundException('No prediction can be found')

        prediction_df = prediction.dataframe
        metadata_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prediction.metadata.items()]))

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        prediction_df.to_excel(writer, sheet_name="Predictions")
        metadata_df.to_excel(writer, sheet_name="Metadata")
        writer.close()
        output.seek(0)

        return f'predictions-{datetime.now()}.xlsx', output

    @classmethod
    def show_dataset_for_adding_targets(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')

        return cls._create_data_tables(dataset.dataframe)

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

        return cls._create_data_tables(dataframe)

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

        DiscoveryPersistence.save_dataset(Dataset(dataset_name, dataframe))

        return cls._create_data_tables(dataframe)

    @classmethod
    def _create_data_tables(cls, dataframe):
        all_dtos = cls._create_all_dtos(dataframe)
        target_name_list = []
        if dataframe is not None:
            target_name_list = list(dataframe.loc[:, dataframe.columns.str.startswith('Target')])
        return dataframe, all_dtos, target_name_list
