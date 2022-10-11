from datetime import datetime

import numpy as np
import pandas as pd
from werkzeug.datastructures import CombinedMultiDict

from slamd.common.error_handling import DatasetNotFoundException, PlotDataNotFoundException
from slamd.common.slamd_utils import empty, float_if_not_empty
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.experiment.experiment_conductor import ExperimentConductor
from slamd.discovery.processing.experiment.experiment_data import ExperimentData
from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from slamd.discovery.processing.forms.discovery_form import DiscoveryForm
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.prediction import Prediction
from slamd.discovery.processing.strategies.csv_strategy import CsvStrategy
from slamd.discovery.processing.strategies.excel_strategy import ExcelStrategy


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

        experiment = cls._initialize_experiment(dataset.dataframe, request_body)
        df_with_predictions, scatter_plot, tsne_plot_data = ExperimentConductor.run(experiment)

        prediction = Prediction(dataset_name, df_with_predictions, request_body)
        DiscoveryPersistence.save_prediction(prediction)
        DiscoveryPersistence.save_tsne_plot_data(tsne_plot_data)

        return df_with_predictions, scatter_plot

    @classmethod
    def download_dataset(cls, dataset_name):
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_name)
        if empty(dataset):
            raise DatasetNotFoundException('Dataset with given name not found')
        # Return the CSV as a string. Represent NaNs in the dataframe as a string.
        return CsvStrategy.to_csv(dataset)

    @classmethod
    def download_prediction(cls):
        prediction = DiscoveryPersistence.query_prediction()
        if empty(prediction):
            raise DatasetNotFoundException('No prediction can be found')

        dataset_of_prediction = DiscoveryPersistence.query_dataset_by_name(prediction.dataset_used_for_prediction)
        if empty(dataset_of_prediction):
            raise DatasetNotFoundException('No dataset for the last prediction can be found')

        output = ExcelStrategy.create_prediction_excel(dataset_of_prediction, prediction)

        return f'predictions-{dataset_of_prediction.name}-{datetime.now()}.xlsx', output

    @classmethod
    def _initialize_experiment(cls, dataframe, request_body):
        target_weights = [float(conf['weight']) for conf in request_body['target_configurations']]
        target_thresholds = [float_if_not_empty(conf['threshold']) for conf in request_body['target_configurations']]
        target_max_or_min = [conf['max_or_min'] for conf in request_body['target_configurations']]

        apriori_weights = [float(conf['weight']) for conf in request_body['a_priori_information_configurations']]
        apriori_thresholds = [float_if_not_empty(conf['threshold'])
                              for conf in request_body['a_priori_information_configurations']]
        apriori_max_or_min = [conf['max_or_min'] for conf in request_body['a_priori_information_configurations']]

        return ExperimentData(
            dataframe=dataframe,
            model=request_body['model'],
            curiosity=float(request_body['curiosity']),
            feature_names=request_body['materials_data_input'],

            target_names=request_body['target_properties'],
            target_weights=target_weights,
            target_thresholds=target_thresholds,
            target_max_or_min=target_max_or_min,

            apriori_names=request_body['a_priori_information'],
            apriori_weights=apriori_weights,
            apriori_thresholds=apriori_thresholds,
            apriori_max_or_min=apriori_max_or_min,
        )

    @classmethod
    def create_tsne_plot(cls):
        tsne_plot_data = DiscoveryPersistence.get_session_tsne_plot_data()
        if not tsne_plot_data:
            raise PlotDataNotFoundException("Cannot find data to create TSNE plot!")

        plot_df = tsne_plot_data.features_df.copy()
        features_std = plot_df.std().replace(0, 1)
        features_mean = plot_df.mean()
        plot_df = (plot_df - features_mean) / features_std

        plot_df['is_train_data'] = 'Predicted'
        plot_df.loc[tsne_plot_data.index_all_labelled, 'is_train_data'] = 'Labelled'

        plot_df['Utility'] = -np.inf
        plot_df.loc[tsne_plot_data.index_none_labelled, 'Utility'] = pd.Series(tsne_plot_data.utility).values
        plot_df = plot_df.sort_values(by='Utility', ascending=False)

        # Number the rows from 1 to n (length of the dataframe) to identify them easier on the plots.
        plot_df.insert(loc=0, column='Row number', value=[i for i in range(1, len(plot_df) + 1)])

        return PlotGenerator.create_tsne_input_space_plot(plot_df)
