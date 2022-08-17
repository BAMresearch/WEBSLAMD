from slamd.common.slamd_utils import empty
from slamd.materials.processing.materials_facade import MaterialsFacade


class WeightInputPreprocessor:

    @classmethod
    def collect_weights_for_creation_of_formulation_batch(cls, materials_data):
        weights_for_all_materials = []
        for material_data in materials_data:
            weights_for_all_materials.append(cls._create_weights(material_data))
        return weights_for_all_materials

    @classmethod
    def collect_base_names_and_weights(cls, formulation_config, constrained=True):
        all_materials_weights = []
        all_names = []
        for i, entry in enumerate(formulation_config):
            material = MaterialsFacade.get_material(entry['type'], entry['uuid'])
            base_names_for_blended_material = cls._add_created_from_base_names(material, entry['type'])
            all_names.append(base_names_for_blended_material)

            if constrained and i == len(formulation_config) - 1:
                continue

            cls._extend_all_weights(all_materials_weights, entry, material)

        # all_materials_weights contains unconstrained weights in terms of the base materials, e.g.
        # all_materials_weights=[['3.64/14.56', '5.74/22.96', '7.84/31.36'], ['15.2', '20.3']]
        return all_materials_weights, all_names

    @classmethod
    def _extend_all_weights(cls, all_materials_weights, entry, material):
        blending_ratios = material.blending_ratios
        weights_for_material = cls._create_weights_for_material(blending_ratios, entry)
        all_materials_weights.append(weights_for_material)

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
    def _create_weights_for_material(cls, blending_ratios, material_configuration):
        if empty(blending_ratios):
            return cls._create_weights(material_configuration)

        ratios = blending_ratios.split('/')
        weights_for_blends = cls._create_weights(material_configuration)

        weights_for_all_base_materials_of_blend = []
        for weight in weights_for_blends:
            weights_of_base_material = ''
            for ratio in ratios:
                weights_of_base_material += f'{round(float(ratio) * float(weight), 2)}/'
            weights_of_base_material = weights_of_base_material.strip()[:-1]
            weights_for_all_base_materials_of_blend.append(weights_of_base_material)
        return weights_for_all_base_materials_of_blend

    @classmethod
    def _create_weights(cls, material_configuration):
        values_for_given_base_material = []
        current_value = float(material_configuration['min'])
        max = float(material_configuration['max'])
        increment = float(material_configuration['increment'])
        while current_value <= max:
            values_for_given_base_material.append(str(round(current_value, 2)))
            current_value += increment
        return values_for_given_base_material
