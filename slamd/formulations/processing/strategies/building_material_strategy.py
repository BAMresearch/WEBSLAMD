from abc import ABC, abstractmethod
from itertools import product

from slamd.common.common_validators import validate_ranges
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException, \
    MaterialNotFoundException
from slamd.common.ml_utils import concat
from slamd.common.slamd_utils import empty, not_numeric, float_if_not_empty
from slamd.discovery.processing.discovery_facade import DiscoveryFacade
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_converter import FormulationsConverter
from slamd.formulations.processing.weight_input_preprocessor import MAX_NUMBER_OF_WEIGHTS, WeightInputPreprocessor
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations

WEIGHT_FORM_DELIMITER = '/'
MAX_DATASET_SIZE = 10000


class BuildingMaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_min_max_form(cls, formulation_selection):
        pass

    @classmethod
    @abstractmethod
    def populate_selection_form(cls):
        pass

    @classmethod
    @abstractmethod
    def get_formulations(cls):
        pass

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
    @abstractmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, type):
        pass

    @classmethod
    def _populate_common_ingredient_selection(cls, form, all_materials):
        form.powder_selection.choices = cls._to_selection(all_materials.powders)
        form.liquid_selection.choices = cls._to_selection(all_materials.liquids)
        form.aggregates_selection.choices = cls._to_selection(all_materials.aggregates_list)
        form.admixture_selection.choices = cls._to_selection(all_materials.admixtures)
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)
        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.name}'), by_type))

    @classmethod
    def _check_for_invalid_material_lists(cls, *material_lists):
        for material_list in material_lists:
            if len(material_list) == 0:
                return True
        return False

    @classmethod
    def _create_process_fields(cls, formulation_selection, min_max_form):
        selection_for_type = [item for item in formulation_selection if item['type'] == 'Process']
        for item in selection_for_type:
            cls._create_min_max_form_entry(min_max_form.process_entries, item['uuid'], item['name'], 'Process')

    @classmethod
    def _get_constrained_weights(cls, formulation_config, weight_constraint):
        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not cls._weight_ranges_valid(formulation_config, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights = WeightInputPreprocessor.collect_weights(formulation_config)

        return cls._compute_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    @abstractmethod
    def _compute_weights_product(cls, all_materials_weights, weight_constraint):
        pass

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
        return cls._sort_materials(materials_for_formulation)

    @classmethod
    @abstractmethod
    def _sort_materials(cls, materials_for_formulation):
        pass

    @classmethod
    def _create_formulation_batch_internal(cls, formulations_data, filename):
        previous_batch_df = DiscoveryFacade.query_dataset_by_name(filename)

        materials_data = formulations_data['materials_request_data']['materials_formulation_configuration']
        processes_data = formulations_data['processes_request_data']['processes']
        weights_data = formulations_data['weights_request_data']['all_weights']
        sampling_size = float_if_not_empty(formulations_data['sampling_size'])

        materials = cls._prepare_materials_for_taking_direct_product(materials_data)

        processes = []
        for process in processes_data:
            processes.append(MaterialsFacade.get_process(process['uuid']))

        if len(processes) > 0:
            materials.append(processes)

        combinations_for_formulations = list(product(*materials))

        dataframe = FormulationsConverter.formulation_to_df(combinations_for_formulations, weights_data)
        if sampling_size < 1:
            dataframe = dataframe.sample(frac=sampling_size)

        if previous_batch_df:
            dataframe = concat(previous_batch_df.dataframe, dataframe)

        if len(dataframe.index) > MAX_DATASET_SIZE:
            raise SlamdRequestTooLargeException(
                f'Formulation is too large. At most {MAX_DATASET_SIZE} rows can be created!')

        dataframe['Idx_Sample'] = range(0, len(dataframe))
        dataframe.insert(0, 'Idx_Sample', dataframe.pop('Idx_Sample'))

        temporary_dataset = Dataset(name=filename, dataframe=dataframe)
        DiscoveryFacade.save_and_overwrite_dataset(temporary_dataset, filename)

        return dataframe

    @classmethod
    def _create_min_max_form_entry_internal(cls, entries, uuids, name, type, req_types, disabled_type):
        entry = entries.append_entry()
        entry.materials_entry_name.data = name
        entry.uuid_field.data = uuids
        entry.type_field.data = type
        if type in req_types:
            entry.increment.name = type
            entry.min.name = type
            entry.max.name = type
        if type == disabled_type:
            entry.increment.render_kw = {'disabled': 'disabled'}
            entry.min.render_kw = {'disabled': 'disabled'}
            entry.max.render_kw = {'disabled': 'disabled'}
            entry.min.label.text = 'Max (kg)'
            entry.max.label.text = 'Min (kg)'
