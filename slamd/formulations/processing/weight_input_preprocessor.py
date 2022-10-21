from slamd.materials.processing.materials_facade import MaterialsFacade

MAX_NUMBER_OF_WEIGHTS = 10000


class WeightInputPreprocessor:

    @classmethod
    def collect_weights(cls, formulation_config):
        # Skip last entry - dependent aggregate or powder
        return [cls._create_weights(entry) for entry in formulation_config[:-1]]

    @classmethod
    def _create_weights(cls, material_configuration):
        values_for_given_material = []
        current_value = float(material_configuration['min'])
        max_value = float(material_configuration['max'])
        increment = float(material_configuration['increment'])

        while current_value <= max_value:
            values_for_given_material.append(str(round(current_value, 2)))

            # Round to prevent floating point errors - everything happens with 2 decimals of precision anyway
            current_value = round(current_value + increment, 2)

        return values_for_given_material
