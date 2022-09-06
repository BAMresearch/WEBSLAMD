from datetime import datetime

from werkzeug.datastructures import CombinedMultiDict

from slamd.common.error_handling import DatasetNotFoundException
from slamd.common.slamd_utils import empty
from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment
from slamd.discovery.processing.algorithms.prediction_output_file_generator import PredictionOutputFileGenerator
from slamd.discovery.processing.algorithms.user_input import UserInput
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.forms.discovery_form import DiscoveryForm
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
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

        prediction = Prediction(dataset_name, df_with_predictions, request_body)
        DiscoveryPersistence.save_prediction(prediction)

        return df_with_predictions, plot

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
        dataset_of_prediction = DiscoveryPersistence.query_dataset_by_name(prediction.dataset_used_for_prediction)

        if empty(prediction):
            raise DatasetNotFoundException('No prediction can be found')

        output = PredictionOutputFileGenerator.create_prediction_xlsx(dataset_of_prediction, prediction)

        return f'predictions-{dataset_of_prediction.name}-{datetime.now()}.xlsx', output

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
