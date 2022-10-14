from abc import ABC, abstractmethod

from slamd.common.common_validators import validate_ranges
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.slamd_utils import empty, not_numeric
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.weight_input_preprocessor import MAX_NUMBER_OF_WEIGHTS, WeightInputPreprocessor

WEIGHT_FORM_DELIMITER = '/'


class BuildingMaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_min_max_form(cls, formulation_selection):
        pass

    @classmethod
    def populate_weigths_form(cls, weights_request_data):
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
    def _invalid_material_combination(cls, *names):
        for name in names:
            if len(name) == 0:
                return True
        return False

    @classmethod
    def _create_non_editable_entries(cls, formulation_selection, min_max_form, type):
        selection_for_type = [item for item in formulation_selection if item['type'] == type]
        for item in selection_for_type:
            cls._create_min_max_form_entry(min_max_form.non_editable_entries, item['uuid'], item['name'], type)

    @classmethod
    def _get_constrained_weights(cls, formulation_config, weight_constraint):
        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not cls._weight_ranges_valid(formulation_config, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights = WeightInputPreprocessor.collect_weights(formulation_config)

        return cls._compute_weigths_product(all_materials_weights, weight_constraint)

    @classmethod
    @abstractmethod
    def _compute_weigths_product(cls, all_materials_weights, weight_constraint):
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
