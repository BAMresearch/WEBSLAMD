from dataclasses import dataclass

from slamd.common.common_validators import min_max_increment_config_valid
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.slamd_utils import not_numeric, not_empty, empty
from slamd.formulations.processing.base_weights_calculator import BaseWeightsCalculator
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.materials.processing.materials_facade import MaterialsFacade

MAX_NUMBER_OF_WEIGHTS = 100


class FormulationsService:

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()

        form = MaterialsAndProcessesSelectionForm()
        form.powder_selection.choices.extend(cls._to_selection(all_materials.powders))
        form.liquid_selection.choices.extend(cls._to_selection(all_materials.liquids))
        form.aggregates_selection.choices.extend(cls._to_selection(all_materials.aggregates_list))
        form.admixture_selection.choices.extend(cls._to_selection(all_materials.admixtures))
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)

        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, count_materials, count_processes):
        if not_empty(count_materials) and not_numeric(count_materials):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_processes) and not_numeric(count_processes):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_materials):
            count_materials = int(count_materials)

        if not_empty(count_processes):
            count_processes = int(count_processes)

        min_max_form = FormulationsMinMaxForm()
        for i in range(count_materials):
            min_max_form.materials_min_max_entries.append_entry()

        for i in range(count_processes):
            min_max_form.processes_entries.append_entry()

        return min_max_form

    @classmethod
    def create_weights_form(cls, weights_request_data):
        materials_formulation_config = weights_request_data['materials_formulation_configuration']
        weight_constraint = weights_request_data['weight_constraint']

        if empty(weight_constraint):
            full_cartesian_product, all_names = cls._get_unconstrained_base_weights(materials_formulation_config)
        else:
            full_cartesian_product, all_names = cls._get_constrained_base_weights(materials_formulation_config,
                                                                       weight_constraint)
        if len(full_cartesian_product) > MAX_NUMBER_OF_WEIGHTS:
            raise SlamdRequestTooLargeException(
                f'Too many weights were requested. At most {MAX_NUMBER_OF_WEIGHTS} weights can be created!')

        weights_form = WeightsForm()
        for i, entry in enumerate(full_cartesian_product):
            ratio_form_entry = weights_form.all_weights_entries.append_entry()
            ratio_form_entry.weights.data = '  |  '.join(entry)
            ratio_form_entry.idx.data = str(i)
        base_names = '  |  '.join(all_names)
        return weights_form, base_names.strip()

    @classmethod
    def _get_constrained_base_weights(cls, materials_formulation_config, weight_constraint):
        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not min_max_increment_config_valid(materials_formulation_config, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights, all_names = cls._collect_base_names_and_weights(materials_formulation_config)

        full_cartesian_product = BaseWeightsCalculator.compute_full_cartesian_product(all_materials_weights,
                                                                                      materials_formulation_config,
                                                                                      weight_constraint)
        return full_cartesian_product, all_names

    @classmethod
    def _get_unconstrained_base_weights(cls, materials_formulation_configuration):
        if not cls._unconstrained_min_max_increment_config_valid(materials_formulation_configuration):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights, all_names = cls._collect_base_names_and_weights(materials_formulation_configuration, False)
        full_cartesian_product = BaseWeightsCalculator.compute_cartesian_product(all_materials_weights)
        return full_cartesian_product, all_names

    @classmethod
    def _collect_base_names_and_weights(cls, materials_formulation_configuration, constrained=True):
        all_materials_weights = []
        all_names = []
        for i in range(len(materials_formulation_configuration)):
            material_uuid = materials_formulation_configuration[i]['uuid']
            material_type = materials_formulation_configuration[i]['type']
            material = MaterialsFacade.get_material(material_type, material_uuid)

            base_names_for_blended_material = cls._add_created_from_base_names(material, material_type)
            all_names.append(base_names_for_blended_material)
            if constrained:
                if i != len(materials_formulation_configuration) - 1:
                    blending_ratios = material.blending_ratios
                    weights_for_material = cls._create_weights_for_material(material.name, blending_ratios,
                                                                            materials_formulation_configuration[i])
                    all_materials_weights.append(weights_for_material)
            else:
                blending_ratios = material.blending_ratios
                weights_for_material = cls._create_weights_for_material(material.name, blending_ratios,
                                                                        materials_formulation_configuration[i])
                all_materials_weights.append(weights_for_material)

        return all_materials_weights, all_names

    @classmethod
    def _add_created_from_base_names(cls, material, material_type):
        base_names_for_blended_material = []
        if material.created_from is None:
            base_names_for_blended_material.append(material.name)
        else:
            for base_uuid in material.created_from:
                base_material = MaterialsFacade.get_material(material_type, str(base_uuid))
                base_names_for_blended_material.append(base_material.name)
        return '/'.join(base_names_for_blended_material)

    @classmethod
    def _create_weights_for_material(cls, material_name, blending_ratios, material_configuration):
        if empty(blending_ratios):
            return MaterialsWeights(material_name=material_name, weights=cls._create_weigths(material_configuration))

        ratios = blending_ratios.split('/')
        weights_for_blends = cls._create_weigths(material_configuration)

        weights_for_all_base_materials_of_blend = []
        for weight in weights_for_blends:
            weights_of_base_material = ''
            for ratio in ratios:
                weights_of_base_material += f'{round(float(ratio) * float(weight), 2)}/'
            weights_of_base_material = weights_of_base_material.strip()[:-1]
            weights_for_all_base_materials_of_blend.append(weights_of_base_material)
        return MaterialsWeights(material_name=material_name, weights=weights_for_all_base_materials_of_blend)

    @classmethod
    def _create_weigths(cls, material_configuration):
        values_for_given_base_material = []
        current_value = float(material_configuration['min'])
        max = float(material_configuration['max'])
        increment = float(material_configuration['increment'])
        while current_value <= max:
            values_for_given_base_material.append(str(round(current_value, 2)))
            current_value += increment
        return values_for_given_base_material

    @classmethod
    def _unconstrained_min_max_increment_config_valid(cls, materials_formulation_configuration):
        for i in range(len(materials_formulation_configuration) - 1):
            min_value = float(materials_formulation_configuration[i]['min'])
            max_value = float(materials_formulation_configuration[i]['max'])
            increment = float(materials_formulation_configuration[i]['increment'])
            if cls._validate_unconstrained_ranges(increment, max_value, min_value):
                return False
        return True

    @classmethod
    def _validate_unconstrained_ranges(cls, increment, max_value, min_value):
        return min_value < 0 or min_value > max_value or max_value < 0 or increment <= 0 or not_numeric(max_value) \
               or not_numeric(min_value) or not_numeric(increment)


"""
Weights are defined at the level of base materials which were used for blending. The material_name refers to the name
of the material used for creating a formulation. This can either be a blended material or a base material. In the latter
case, the weights simply correspond to the weigth passed in the input fields. 
"""


@dataclass
class MaterialsWeights:
    material_name: str
    weights: list[str]
