

import math

import numpy as np

from slamd.common.error_handling import DatasetNotFoundException, ValueNotSupportedException
from slamd.common.slamd_utils import empty, not_numeric, not_empty, float_if_not_empty
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.extend_page_data import ExtendPageData
from slamd.discovery.processing.forms.extend_form import ExtendForm


class ExtendService:

    @classmethod
    def get_data_for_extend_page(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        return cls._create_extend_page_data(dataset)

    @classmethod
    def _create_extend_page_data(cls, dataset):
        dataframe = dataset.dataframe
        extend_form = ExtendForm()
        extend_form.select_columns.choices = dataset.columns
        extend_form.target_columns.choices = dataset.columns
        return ExtendPageData(dataframe, extend_form)

    @classmethod
    def generate_samples(cls, df, num_samples, selected_columns, min_values, max_values, target_columns):
<<<<<<< Updated upstream
=======
        new_df = df.copy()

>>>>>>> Stashed changes
        for i in range(num_samples):
            sample_row = {}
            for col in df.columns:
                if col in target_columns:
                    sample_row[col] = np.nan
                elif col in selected_columns:
                    min_value = min_values[col]
                    max_value = max_values[col]
                    sample_row[col] = np.random.uniform(min_value, max_value)
                else:
                    sample_row[col] = df[col].sample(1).values[0]
<<<<<<< Updated upstream
            df = df.append(sample_row, ignore_index=True)
        return df
=======
            new_df = new_df.append(sample_row, ignore_index=True)
        return new_df
>>>>>>> Stashed changes

