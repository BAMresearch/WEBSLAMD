from itertools import product

from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.ml_utils import concat
from slamd.common.slamd_utils import empty
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CEMENT_FORMULATION
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.building_material_strategy import BuildingMaterialStrategy, WEIGHT_FORM_DELIMITER
from slamd.formulations.processing.forms.cement_selection_form import CementSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_converter import FormulationsConverter
from slamd.formulations.processing.weight_input_preprocessor import MAX_NUMBER_OF_WEIGHTS
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade

MAX_DATASET_SIZE = 10000


class CementStrategy(BuildingMaterialStrategy):

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()
        form = cls._populate_common_ingredient_selection(CementSelectionForm(), all_materials)
        return form, BuildingMaterial.CEMENT.value

    @classmethod
    def get_formulations(cls):
        dataframe = None
        temporary_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_CEMENT_FORMULATION)
        if temporary_dataset:
            dataframe = temporary_dataset.dataframe
        return dataframe

    @classmethod
    def create_min_max_form(cls, formulation_selection):
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

        if cls._invalid_material_combination(liquid_names, powder_names):
            raise ValueNotSupportedException('You need to specify at least one powder and one liquid')

        min_max_form = FormulationsMinMaxForm()

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(liquid_uuids),
                                       'W/C Ratio', 'Liquid')

        min_max_form.materials_min_max_entries.entries[-1].increment.label.text = 'Increment (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].min.label.text = 'Min (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].max.label.text = 'Max (W/C-ratio)'

        if len(aggregates_names):
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                           'Aggregates ({0})'.format(', '.join(aggregates_names)), 'Aggregates')

        if len(admixture_names):
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(admixture_uuids),
                                           'Admixtures ({0})'.format(', '.join(admixture_names)), 'Admixture')

        if len(custom_names):
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(custom_uuids),
                                           'Customs ({0})'.format(', '.join(custom_names)), 'Custom')

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(powder_uuids),
                                       'Powders ({0})'.format(', '.join(powder_names)), 'Powder')

        cls._create_process_fields(formulation_selection, min_max_form)

        min_max_form.liquid_info_entry.data = 'Liquids ({0})'.format(', '.join(liquid_names))

        return min_max_form

    @classmethod
    def populate_weights_form(cls, weights_request_data):
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
    def create_formulation_batch(cls, formulations_data):
        previous_batch_df = DiscoveryFacade.query_dataset_by_name(TEMPORARY_CEMENT_FORMULATION)

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

        temporary_dataset = Dataset(name=TEMPORARY_CEMENT_FORMULATION, dataframe=dataframe)
        DiscoveryFacade.save_temporary_dataset(temporary_dataset, TEMPORARY_CEMENT_FORMULATION)

        return dataframe

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, type):
        entry = entries.append_entry()
        entry.materials_entry_name.data = name
        entry.uuid_field.data = uuids
        entry.type_field.data = type
        if type == 'Powder' or type == 'Liquid':
            entry.increment.name = type
            entry.min.name = type
            entry.max.name = type
        if type == 'Powder':
            entry.increment.render_kw = {'disabled': 'disabled'}
            entry.min.render_kw = {'disabled': 'disabled'}
            entry.max.render_kw = {'disabled': 'disabled'}
            entry.min.label.text = 'Max (kg)'
            entry.max.label.text = 'Min (kg)'

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, weight_constraint):
        return WeightsCalculator.compute_full_cement_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_cement_formulation(materials_for_formulation)
