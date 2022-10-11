from itertools import product
from datetime import datetime

from werkzeug.utils import secure_filename

from slamd.common.common_validators import validate_ranges
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException, \
    MaterialNotFoundException
from slamd.common.slamd_utils import not_numeric, empty
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_FORMULATION
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_converter import FormulationsConverter
from slamd.formulations.processing.weight_input_preprocessor import WeightInputPreprocessor
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations
from slamd.common.ml_utils import concat

WEIGHT_FORM_DELIMITER = '/'
MAX_NUMBER_OF_WEIGHTS = 10000
MAX_DATASET_SIZE = 10000


class FormulationsService:

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()

        form = MaterialsAndProcessesSelectionForm()
        form.powder_selection.choices = cls._to_selection(all_materials.powders)
        form.liquid_selection.choices = cls._to_selection(all_materials.liquids)
        form.aggregates_selection.choices = cls._to_selection(all_materials.aggregates_list)
        form.admixture_selection.choices = cls._to_selection(all_materials.admixtures)
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)

        return form

    @classmethod
    def get_formulations(cls):
        dataframe = None
        temporary_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_FORMULATION)
        if temporary_dataset:
            dataframe = temporary_dataset.dataframe
        return dataframe

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, formulation_selection):
        powder_names = [item['name'] for item in formulation_selection if item['type'] == 'Powder']
        liquid_names = [item['name'] for item in formulation_selection if item['type'] == 'Liquid']
        aggregates_names = [item['name'] for item in formulation_selection if item['type'] == 'Aggregates']
        admixture_names = [item['name'] for item in formulation_selection if item['type'] == 'Admixture']
        custom_names = [item['name'] for item in formulation_selection if item['type'] == 'Custom']

        powder_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Powder']
        liquid_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Liquid']
        aggregates_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Aggregates']
        admixture_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Admixture']
        custom_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Custom']

        if len(powder_names) == 0 or len(liquid_names) == 0 or len(aggregates_names) == 0:
            raise ValueNotSupportedException('You need to specify powders, liquids and aggregates')

        min_max_form = FormulationsMinMaxForm()

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(powder_uuids),
                                       'Powders ({0})'.format(', '.join(powder_names)), 'Powder')
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(liquid_uuids),
                                       'Liquids ({0})'.format(', '.join(liquid_names)), 'Liquid')

        min_max_form.materials_min_max_entries.entries[-1].increment.label.text = 'Increment (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].min.label.text = 'Min (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].max.label.text = 'Max (W/C-ratio)'

        if len(admixture_names):
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(admixture_uuids),
                                           'Admixtures ({0})'.format(', '.join(admixture_names)), 'Admixture')

        if len(custom_names):
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(custom_uuids),
                                           'Customs ({0})'.format(', '.join(custom_names)), 'Custom')

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                       'Aggregates ({0})'.format(', '.join(aggregates_names)), 'Aggregates')

        cls._create_non_editable_entries(formulation_selection, min_max_form, 'Process')

        return min_max_form

    @classmethod
    def _create_non_editable_entries(cls, formulation_selection, min_max_form, type):
        selection_for_type = [item for item in formulation_selection if item['type'] == type]
        for item in selection_for_type:
            cls._create_min_max_form_entry(min_max_form.non_editable_entries, item['uuid'], item['name'], type)

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, type):
        entry = entries.append_entry()
        entry.materials_entry_name.data = name
        entry.uuid_field.data = uuids
        entry.type_field.data = type
        if type == 'Powder' or type == 'Liquid' or type == 'Aggregates':
            entry.increment.name = type
            entry.min.name = type
            entry.max.name = type
        if type == 'Aggregates':
            entry.increment.render_kw = {'disabled': 'disabled'}
            entry.min.render_kw = {'disabled': 'disabled'}
            entry.max.render_kw = {'disabled': 'disabled'}
            entry.min.label.text = 'Max (kg)'
            entry.max.label.text = 'Min (kg)'

    @classmethod
    def create_weights_form(cls, weights_request_data):
        materials_formulation_config = weights_request_data['materials_formulation_configuration']
        weight_constraint = weights_request_data['weight_constraint']

        # the result of the computation contains a list of lists with each containing the weights in terms of the
        # various materials used for blending; for example weight_combinations =
        # "[['18.2', '15.2', '66.6'], ['18.2', '20.3', '61.5'], ['28.7', '15.2', '56.1']]"
        if empty(weight_constraint):
            raise ValueNotSupportedException('You must set a non-empty weight constraint!')
        else:
            weight_combinations = cls._get_constrained_weights(materials_formulation_config, weight_constraint)

        if len(weight_combinations) > MAX_NUMBER_OF_WEIGHTS:
            raise SlamdRequestTooLargeException(
                f'Too many weights were requested. At most {MAX_NUMBER_OF_WEIGHTS} weights can be created!')

        weights_form = WeightsForm()
        for i, entry in enumerate(weight_combinations):
            ratio_form_entry = weights_form.all_weights_entries.append_entry()
            ratio_form_entry.weights.data = WEIGHT_FORM_DELIMITER.join(entry)
            ratio_form_entry.idx.data = str(i)
        return weights_form

    @classmethod
    def _get_constrained_weights(cls, formulation_config, weight_constraint):
        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not cls._weight_ranges_valid(formulation_config, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights = WeightInputPreprocessor.collect_weights(formulation_config)

        return WeightsCalculator.compute_full_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    def _weight_ranges_valid(cls, formulation_config, constraint):
        # Skip aggregate (last value)
        for i, conf in enumerate(formulation_config[:-1]):
            if i == 1:
                # liquid - ratios, calculate differently
                min_value = float(conf['min']) * float(formulation_config[0]['min'])
                max_value = float(conf['max']) * float(formulation_config[0]['max'])
                # validation checks if increment is negative, 0 or non_numeric - does not need to be multiplied
                increment = float(conf['increment'])
            else:
                # everything else - regular validation
                min_value = float(conf['min'])
                max_value = float(conf['max'])
                increment = float(conf['increment'])

            if validate_ranges(increment, max_value, min_value, float(constraint)):
                return False

        return True

    @classmethod
    def create_materials_formulations(cls, formulations_data):
        previous_batch_df = DiscoveryFacade.query_dataset_by_name(TEMPORARY_FORMULATION)

        materials_data = formulations_data['materials_request_data']['materials_formulation_configuration']
        processes_data = formulations_data['processes_request_data']['processes']
        weights_data = formulations_data['weights_request_data']['all_weights']

        materials = cls._prepare_materials_for_taking_direct_product(materials_data)

        processes = []
        for process in processes_data:
            processes.append(MaterialsFacade.get_process(process['uuid']))

        if len(processes) > 0:
            materials.append(processes)

        combinations_for_formulations = list(product(*materials))

        dataframe = FormulationsConverter.formulation_to_df(combinations_for_formulations, weights_data)

        if previous_batch_df:
            dataframe = concat(previous_batch_df.dataframe, dataframe)

        if len(dataframe.index) > MAX_DATASET_SIZE:
            raise SlamdRequestTooLargeException(
                f'Formulation is too large. At most {MAX_DATASET_SIZE} rows can be created!')

        dataframe['Idx_Sample'] = range(0, len(dataframe))
        dataframe.insert(0, 'Idx_Sample', dataframe.pop('Idx_Sample'))

        temporary_dataset = Dataset(name=TEMPORARY_FORMULATION, dataframe=dataframe)
        DiscoveryFacade.save_temporary_dataset(temporary_dataset)

        return dataframe

    @classmethod
    def _prepare_materials_for_taking_direct_product(cls, materials_data):
        powders = []
        liquids = []
        aggregates = []
        admixtures = []
        customs = []
        for materials_for_type_data in materials_data:
            uuids = materials_for_type_data['uuids'].split(',')
            for uuid in uuids:
                material_type = materials_for_type_data['type']
                if material_type.lower() == MaterialsFacade.POWDER:
                    powders.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.LIQUID:
                    liquids.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.AGGREGATES:
                    aggregates.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.ADMIXTURE:
                    admixtures.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.CUSTOM:
                    customs.append(MaterialsFacade.get_material(material_type, uuid))
                else:
                    raise MaterialNotFoundException('Cannot process the requested material!')

        # We sort the materials according to a) the fact that for concrete, aggregates is always the dependent material
        # in terms of the weight constraint thus appearing last and b) the order of appearance in the formulation UI
        materials_for_formulation = MaterialsForFormulations(powders, aggregates, liquids, admixtures, customs)
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)

    @classmethod
    def _create_properties(cls, inner_dict):
        properties = ''
        for key, value in inner_dict.items():
            properties += f'{key}: {value}; '
        properties = properties.strip()[:-1]
        return properties

    @classmethod
    def _create_targets(cls, inner_dict, targets):
        targets_as_dto = []
        target_list = targets.split(';')
        target_dict = {k: v for k, v in inner_dict.items() if k in target_list}
        for key, value in target_dict.items():
            targets_as_dto.append(value)
        return targets_as_dto

    @classmethod
    def delete_formulation(cls):
        DiscoveryFacade.delete_dataset_by_name(TEMPORARY_FORMULATION)

    @classmethod
    def save_dataset(cls, form):
        filename = cls._sanitize_filename(form['dataset_name'])
        formulation_to_be_saved_as_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_FORMULATION)
        DiscoveryFacade.delete_dataset_by_name(TEMPORARY_FORMULATION)
        formulation_to_be_saved_as_dataset.name = filename
        if formulation_to_be_saved_as_dataset:
            DiscoveryFacade.save_dataset(formulation_to_be_saved_as_dataset)

    @classmethod
    def _sanitize_filename(cls, user_input):
        if user_input == '':
            # Generate a filename to allow the user to create many datasets
            # one after the other, without having to enter a filename.
            user_input = f'Unnamed-Dataset-{datetime.now()}'

        if not user_input.endswith('.csv'):
            # Add the extension to make it clear which format the app supports
            # for downloading datasets. This may change in the future.
            user_input = user_input + '.csv'

        filename = secure_filename(user_input)
        if filename == TEMPORARY_FORMULATION:
            raise ValueNotSupportedException('You cannot use the name temporary for your dataset!')
        return filename
