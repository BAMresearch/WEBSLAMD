from dataclasses import dataclass

from slamd.common.common_validators import min_max_increment_config_valid
from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import not_numeric, not_empty, empty
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.materials.processing.materials_persistence import MaterialsPersistence

MAX_NUMBER_OF_WEIGHTS = 100


class FormulationsService:

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsPersistence.find_all_materials()

        flattened_materials = []
        for materials_for_type in all_materials:
            for material in materials_for_type:
                flattened_materials.append(material)

        materials_for_selection = cls._to_selection(flattened_materials)

        all_processes = MaterialsPersistence.find_all_processes()
        processes_for_selection = cls._to_selection(all_processes)

        form = MaterialsAndProcessesSelectionForm()
        form.material_selection.choices = materials_for_selection
        form.process_selection.choices = processes_for_selection

        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (
            f'{material.type}|{str(material.uuid)}', f'{material.type.capitalize()}: {material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, count_materials, count_processes):
        if not_numeric(count_materials):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_processes) and not_numeric(count_processes):
            raise ValueNotSupportedException('Cannot process selection!')

        count_materials = int(count_materials)

        if not_empty(count_processes):
            count_processes = int(count_processes)

        if count_materials == 0:
            raise ValueNotSupportedException('No material selected!')

        min_max_form = FormulationsMinMaxForm()
        for i in range(count_materials):
            min_max_form.materials_min_max_entries.append_entry()

        for i in range(count_processes):
            min_max_form.processes_entries.append_entry()

        return min_max_form

    @classmethod
    def create_weights_form(cls, weights_request_data):
        materials_formulation_configuration = weights_request_data['materials_formulation_configuration']
        weight_constraint = weights_request_data['weight_constraint']

        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')

        if not min_max_increment_config_valid(materials_formulation_configuration, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights = []
        for material_configuration in materials_formulation_configuration:
            material_uuid = material_configuration['uuid']
            material_type = material_configuration['type']
            material = MaterialsPersistence.query_by_type_and_uuid(material_type, material_uuid)
            blending_ratios = material.blending_ratios
            weights_for_material = cls._create_weights_for_material(material.name, blending_ratios,
                                                                    materials_formulation_configuration)
            all_materials_weights.append(weights_for_material)

        return []

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
        for i in range(len(material_configuration) - 1):
            values_for_given_base_material = []
            current_value = float(material_configuration[i]['min'])
            max = float(material_configuration[i]['max'])
            increment = float(material_configuration[i]['increment'])
            while current_value <= max:
                values_for_given_base_material.append(str(current_value))
                current_value += increment
            return values_for_given_base_material


"""
Weights are defined at the level of base materials which were used for blending. The material_name refers to the name
of the material used for creating a formulation. This can either be a blended material or a base material. In the latter
case, the weights simply correspond to the weigth passed in the input fields. 
"""
@dataclass
class MaterialsWeights:
    material_name: str
    weights: list[str]
