from itertools import product

AIR_PORE_CONTENT_VOLUME = 0.02
# Factor to compute volume of material in m3 based on specific gravity in g/cm3 and mass in kg
G_CM3_TO_KG_M3_CONVERSION_FACTOR = 1000


class VolumesCalculator:

    @classmethod
    def compute_volumes_from_weights(cls, weights, specific_gravities, admixture_custom_indices):
        volumes = []
        admixture_index = admixture_custom_indices.get('admixture_index')
        custom_index = admixture_custom_indices.get('custom_index')
        admixture_weights = weights[admixture_index] if admixture_index else None
        custom_weights = weights[custom_index] if custom_index else None

        for specific_gravity in specific_gravities:
            if specific_gravity.get('type') == 'Powder':
                powder_volumes = [float(powder_weight) / (float(specific_gravity.get('specific_gravity')) * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
                                         for powder_weight in weights[0]]
                powder_uuid = specific_gravity.get('uuid')
                volumes.append({'type': 'Powder', 'uuid': powder_uuid, 'volumes': powder_volumes})
            if specific_gravity.get('type') == 'Liquid':
                liquid_volumes = [float(liquid_weight) / (float(specific_gravity.get('specific_gravity')) * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
                                        for liquid_weight in weights[1]]
                liquid_uuid = specific_gravity.get('uuid')
                volumes.append({'type': 'Liquid', 'uuid': liquid_uuid, 'volumes': liquid_volumes})
            if specific_gravity.get('type') == 'Admixture':
                admixture_volumes = [float(admixture_weight) / (float(specific_gravity.get('specific_gravity')) *
                                                                G_CM3_TO_KG_M3_CONVERSION_FACTOR) for admixture_weight in admixture_weights]
                admixture_uuid = specific_gravity.get('uuid')
                volumes.append({'type': 'Admixture', 'uuid': admixture_uuid, 'volumes': admixture_volumes})
            if specific_gravity.get('type') == 'Custom':
                custom_volumes = [float(custom_weight) / (float(specific_gravity.get('specific_gravity')) * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
                                         for custom_weight in custom_weights]
                custom_uuid = specific_gravity.get('uuid')
                volumes.append({'type': 'Custom', 'uuid': custom_uuid, 'volumes': custom_volumes})

        return volumes

    @classmethod
    def generate_volumes_for_combinations(cls, material_combinations):
        combinations_with_volumes = []
        for material_combination in material_combinations:
            volumes = [material['volumes'] for material in material_combination]

            all_combinations = list(product(*volumes))

            new_formulation = [{key: value for key, value in material.items() if key != 'volumes'} for material in
                               material_combination]

            combinations_with_volumes.append({"materials": new_formulation, "all_volumes": all_combinations})

        return combinations_with_volumes

    @classmethod
    def validate_volume_combinations(cls, formulations, volume_constraint):
        for formulation in formulations:
            valid_combinations = []
            all_volumes = formulation.get('all_volumes')

            for combination in all_volumes:
                # if sum(combination) + AIR_PORE_CONTENT_VOLUME < float(volume_constraint):
                if sum(combination) + AIR_PORE_CONTENT_VOLUME < 0.26:
                    valid_combinations.append(combination)
            formulation['all_volumes'] = set(valid_combinations)
        return formulations


    @classmethod
    def add_aggregates_volume_to_combination(cls, formulations, specific_gravities, weight_constraint):
        aggregates = [specific_gravity for specific_gravity in specific_gravities if specific_gravity['type'] == 'Aggregates' ]
        for formulation in formulations:
            for aggregate in aggregates:
                all_volumes = []
                formulation['materials'].append({'type': 'Aggregates', 'uuid': aggregate['uuid']})
                for volume_combination in formulation['all_volumes']:
                    aggregate_volume = float(weight_constraint) - sum(volume_combination) - AIR_PORE_CONTENT_VOLUME
                    volume_combination = (*volume_combination, aggregate_volume)
                    all_volumes.append(volume_combination)
                formulation['all_volumes'] = all_volumes

        return formulations

    @classmethod
    def transform_volumes_to_weights(cls, formulations, specific_gravities, admixture_custom_indices):
        powder_uuid = ''
        liquid_uuid = ''
        admixture_uuid = ''
        custom_uuid = ''
        aggregates_uuid = ''
        for formulation in formulations:
            all_weights = []
            powder_specific_gravity = ''
            liquid_specific_gravity = ''
            aggregates_specific_gravity = ''
            admixture_specific_gravity = ''
            custom_specific_gravity = ''
            for materials in formulation['materials']:
                if materials.get('type') == 'Powder':
                    powder_uuid = materials.get('uuid')
                if materials.get('type') == 'Liquid':
                    liquid_uuid = materials.get('uuid')
                if materials.get('type') == 'Admixture':
                    admixture_uuid = materials.get('uuid')
                if materials.get('type') == 'Custom':
                    custom_uuid = materials.get('uuid')
                if materials.get('type') == 'Aggregates':
                    aggregates_uuid = materials.get('uuid')
            for specific_gravity in specific_gravities:
                specific_gravity_uuid = specific_gravity.get('uuid')
                if specific_gravity_uuid == powder_uuid:
                    powder_specific_gravity = specific_gravity.get('specific_gravity')
                if specific_gravity_uuid == liquid_uuid:
                    liquid_specific_gravity = specific_gravity.get('specific_gravity')
                if specific_gravity_uuid == aggregates_uuid:
                    aggregates_specific_gravity = specific_gravity.get('specific_gravity')
                if specific_gravity_uuid == admixture_uuid:
                    admixture_specific_gravity = specific_gravity.get('specific_gravity')
                if specific_gravity_uuid == custom_uuid:
                    custom_specific_gravity = specific_gravity.get('specific_gravity')

            for formulation_volumes in formulation['all_volumes']:
                formulation_weights = ''
                powder_weight = round(float(formulation_volumes[0]) * float(powder_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)
                formulation_weights += str(powder_weight)
                liquid_weight = round(float(formulation_volumes[1]) * float(liquid_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)
                formulation_weights += '/' + str(liquid_weight)
                aggregate_weight = round(float(formulation_volumes[-1]) * float(aggregates_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)

                if admixture_custom_indices.get('admixture_index'):
                    admixture_weight = round(float(formulation_volumes[2]) * float(admixture_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)
                    formulation_weights += '/' + str(admixture_weight)
                    if admixture_custom_indices.get('custom_index'):
                        custom_weight = round(float(formulation_volumes[3]) * float(custom_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)
                        formulation_weights += '/' + str(custom_weight)
                else:
                    if admixture_custom_indices.get('custom_index'):
                        custom_weight = round(float(formulation_volumes[2]) * float(custom_specific_gravity) * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2)
                        formulation_weights += '/' + str(custom_weight)
                formulation_weights += '/' + str(aggregate_weight)
                all_weights.append(formulation_weights)

            formulation.pop('all_volumes')
            formulation['all_weights'] = all_weights
        return formulations














