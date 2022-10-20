from slamd.common.slamd_utils import string_to_number, not_empty, numeric
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class BlendingPropertiesCalculator:

    @classmethod
    def compute_blended_costs(cls, normalized_ratios, base_materials_as_dict):
        blended_co2_footprint = cls.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'co2_footprint')
        blended_costs = cls.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'costs')
        blended_delivery_time = cls._compute_max(base_materials_as_dict, 'costs', 'delivery_time')

        return Costs(co2_footprint=blended_co2_footprint, costs=blended_costs, delivery_time=blended_delivery_time)

    @classmethod
    def compute_mean(cls, normalized_ratios, materials_as_dict, *keys):
        is_complete, all_values = PropertyCompletenessChecker.is_complete_with_values_returned(materials_as_dict, keys)

        if not is_complete:
            return None

        mean = sum([norm_ratio * string_to_number(value) for (norm_ratio, value) in zip(normalized_ratios, all_values)])
        return round(mean, 2)

    @classmethod
    def _compute_max(cls, material_as_dict, *keys):
        all_values = PropertyCompletenessChecker.collect_all_base_material_values_for_property(material_as_dict, keys)
        non_empty_values = [float(value) for value in all_values if not_empty(value)]
        if len(non_empty_values) == 0:
            return None
        maximum = max(non_empty_values)
        return round(maximum, 2)

    #
    # normalized_ratios: normalized ratios determined from the user input, e.g. [0.4, 0.4, 0.2]
    # base_materials_as_dict: base materials as dictionaries used as input for blending; number of them must match the length of normalized_ratios
    #
    # The algorithm below works as follows (check the corresponding unit tests to see the functionality at work):
    #
    # 1) We first extract the properties which are common to all base materials. Thus, if we have two base materials A and B
    # additional_properties(A): [AdditionalProperty('Prop 1', '2'), AdditionalProperty('Prop 2', '3.2')] and
    # additional_properties(B): [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 3', '3.2'), AdditionalProperty('Prop 5', '3.2')]
    # the result (key_defined_in_all_base_materials) will ['Prop 1'].
    #
    # 2) We collect the common properties of all base materials. In our example this would amount to the following result
    # (matching_properties_for_all_base_materials): [[AdditionalProperty(name='Prop1', value='2')],[AdditionalProperty('Prop 1', '5')]]
    #
    # 3) We zip together the ratios with the result from step 2) to compute the resulting blended additional properties.
    # For that purpose we distinguish continuous and categorical (string) values for the properties.
    #
    # a) If all values for a given property name are numerical we create one blended property with value set by the
    # weighted sum of the base values.
    # b) If for a given name, there are categorical as well as continuous variables, we do not create an additional
    # property for the blend as the description is incomplete.
    # c) For only categoricals for a given name, we create additional properties for each differing value of the categorical
    # with value specified by the corresponding weight.
    #
    # 4) We merge categoricals created in 3c) with the same name and sum up their values.
    #

    @classmethod
    def compute_additional_properties(cls, normalized_ratios, base_materials_as_dict):
        matching_properties_for_all_base_materials = cls._find_properties_contained_in_all_base_materials(
            base_materials_as_dict)

        blended_additional_properties = []
        for i in range(len(matching_properties_for_all_base_materials[0])):
            ratios_with_property_values = zip(normalized_ratios, matching_properties_for_all_base_materials)

            # Create list of property names together with their weighted values and an information about the
            # current ratio, e.g [('Prop1', 1.0, 0.5), ('Prop1', 2.0, 0.5)]
            mapped_properties = [cls._compute_weighted_properties_with_ratios(
                x[0], x[1][i]) for x in ratios_with_property_values]
            if numeric(mapped_properties[0][1]):
                cls._add_continuous_additional_properties(blended_additional_properties, mapped_properties)
            else:
                cls.add_categorical_additional_properties(blended_additional_properties, mapped_properties)
        return blended_additional_properties

    @classmethod
    def _find_properties_contained_in_all_base_materials(cls, base_materials_as_dict):
        properties_with_key_defined_in_all_base_materials = \
            PropertyCompletenessChecker.find_additional_properties_defined_in_all_base_materials(base_materials_as_dict)
        key_defined_in_all_base_materials = [prop.name for prop in properties_with_key_defined_in_all_base_materials]
        matching_properties_for_all_base_materials = []
        for base_material_dict in base_materials_as_dict:
            matching_properties_for_base_material = [
                prop for prop in base_material_dict['additional_properties']
                if prop.name in key_defined_in_all_base_materials
            ]

            matching_properties_for_all_base_materials.append(matching_properties_for_base_material)
        return matching_properties_for_all_base_materials

    @classmethod
    def add_categorical_additional_properties(cls, blended_additional_properties, mapped_properties):
        for item in mapped_properties:
            blended_property_names = [x.name for x in blended_additional_properties]
            if item[1] in blended_property_names:
                index_of_matching_name = blended_property_names.index(item[1])
                updated_value = float(blended_additional_properties[index_of_matching_name].value) + item[2]
                blended_additional_properties[index_of_matching_name].value = str(round(updated_value, 2))
            else:
                blended_additional_properties.append(
                    AdditionalProperty(name=item[1], value=str(round(item[2], 2))))

    @classmethod
    def _add_continuous_additional_properties(cls, blended_additional_properties, mapped_properties):
        mean = sum([prop[1] for prop in mapped_properties])
        blended_additional_properties.append(
            AdditionalProperty(name=mapped_properties[0][0], value=str(round(mean, 2))))

    @classmethod
    def _compute_weighted_properties_with_ratios(cls, ratio, prop):
        return prop.name, cls._map_according_to_value(ratio, prop.value), ratio

    @classmethod
    def _map_according_to_value(cls, ratio, value):
        if numeric(value):
            return ratio * string_to_number(value)
        return value
