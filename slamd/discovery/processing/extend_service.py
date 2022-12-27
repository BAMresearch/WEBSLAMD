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
        extend_form.string_columns.choices = dataset.columns
        extend_form.target_columns.choices = dataset.columns
        return ExtendPageData(dataframe, extend_form)

    @classmethod
    def generate_samples(cls, dataset, num_sample, min_value, max_value, target_columns, string_columns):

        new_df = dataset.copy()

        for i in range(num_sample):
            sample_row = {}
            for col in dataset.columns:
                if col in target_columns:
                    sample_row[col] = np.nan
                elif col in string_columns:
                    sample_row[col] = dataset[col].values[0]
                else:
                    sample_row[col] = round(np.random.uniform(min_value, max_value), 2)

        new_df = new_df.apply(lambda x: round(x, 2) if x.dtype == 'float' else x)

        return new_df
