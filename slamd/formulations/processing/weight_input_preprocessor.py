from slamd.common.error_handling import SlamdRequestTooLargeException
from slamd.materials.processing.materials_facade import MaterialsFacade

MAX_NUMBER_OF_WEIGHTS = 10000


class WeightInputPreprocessor:

    @classmethod
    def collect_weights_for_creation_of_formulation_batch(cls, materials_data):
        weights_for_all_materials = []
        for material_data in materials_data:
            weights_for_all_materials.append(cls._create_weights(material_data))
        return weights_for_all_materials

    @classmethod
    def collect_weights(cls, formulation_config):
        all_materials_weights = []
        total_number_of_weight_combinations = 1
        for i, entry in enumerate(formulation_config):
            if i == len(formulation_config) - 1:
                continue
            weights_for_material = cls._create_weights_for_material(entry)
            all_materials_weights.append(weights_for_material)

            total_number_of_weight_combinations *= len(weights_for_material)

            if total_number_of_weight_combinations >= MAX_NUMBER_OF_WEIGHTS:
                raise SlamdRequestTooLargeException(
                    f'Too many weights were requested. At most {MAX_NUMBER_OF_WEIGHTS} weights can be created!')

        return all_materials_weights

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
    def _create_weights_for_material(cls, material_configuration):
        return cls._create_weights(material_configuration)

    @classmethod
    def _create_weights(cls, material_configuration):
        values_for_given_material = []
        current_value = float(material_configuration['min'])
        max = float(material_configuration['max'])
        increment = float(material_configuration['increment'])
        while current_value <= max:
            values_for_given_material.append(str(round(current_value, 2)))
            current_value += increment
        return values_for_given_material
