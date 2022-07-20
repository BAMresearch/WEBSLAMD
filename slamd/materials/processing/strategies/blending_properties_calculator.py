from functools import reduce

from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import empty, string_to_number, not_empty, numeric, not_numeric
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs


class BlendingPropertiesCalculator:

    @classmethod
    def compute_blended_costs(cls, normalized_ratios, base_materials_as_dict):
        blended_co2_footprint = cls.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'co2_footprint')
        blended_costs = cls.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'costs')
        blended_delivery_time = cls._compute_max(base_materials_as_dict, 'costs', 'delivery_time')

        return Costs(co2_footprint=blended_co2_footprint, costs=blended_costs, delivery_time=blended_delivery_time)

    @classmethod
    def compute_mean(cls, normalized_ratios, materials_as_dict, *keys):
        all_values = cls._collect_all_base_material_values_for_property(materials_as_dict, keys)

        empty_values = [value for value in all_values if empty(value)]

        if len(empty_values) > 0:
            return None

        ratios_with_property_values = zip(normalized_ratios, all_values)
        mean = sum(list(map(lambda x: x[0] * string_to_number(x[1]), ratios_with_property_values)))
        return str(round(mean, 2))

    @classmethod
    def _compute_max(cls, material_as_dict, *keys):
        all_values = cls._collect_all_base_material_values_for_property(material_as_dict, keys)
        non_empty_values = [float(value) for value in all_values if not_empty(value)]
        if len(non_empty_values) == 0:
            return None
        maximum = max(non_empty_values)
        return str(round(maximum, 2))

    @classmethod
    def _collect_all_base_material_values_for_property(cls, material_as_dict, keys):
        all_values = []

        for current_powder in material_as_dict:
            value = cls._extract_value_for_key(current_powder, keys)
            all_values.append(value)

        return all_values

    @classmethod
    def _extract_value_for_key(cls, material_as_dict, keys):
        base = material_as_dict
        for key in keys:
            value = base.get(key, None)
            try:
                base = value.__dict__
            except AttributeError:
                return value

        raise ValueNotSupportedException('No such property!')

    @classmethod
    def compute_additional_properties(cls, normalized_ratios, base_materials_as_dict):
        additional_properties_for_all_base_materials = []
        for base_powder in base_materials_as_dict:
            additional_properties_for_all_base_materials.append(base_powder['additional_properties'])

        properties_with_key_defined_in_all_base_materials = reduce(lambda x, y: cls._keep_matching(x, y),
                                                                   additional_properties_for_all_base_materials)
        key_defined_in_all_base_materials = list(
            map(lambda prop: prop.name, properties_with_key_defined_in_all_base_materials))

        matching_properties_for_all_base_materials = []
        for base_material_dict in base_materials_as_dict:
            matching_properties_for_base_material = list(
                filter(lambda prop: prop.name in key_defined_in_all_base_materials,
                       base_material_dict['additional_properties']))

            matching_properties_for_all_base_materials.append(matching_properties_for_base_material)

        blended_additional_properties = []
        for i in range(len(matching_properties_for_all_base_materials[0])):
            ratios_with_property_values = zip(normalized_ratios, matching_properties_for_all_base_materials)

            # Create list of property names together with their weigthed values and an information about the
            # current ratio, e.g [('Prop1', 1.0, 0.5), ('Prop1', 2.0, 0.5)]
            mapped_properties = list(map(lambda x: cls._compute_weighted_properties_with_ratios(x[0], x[1][i]), ratios_with_property_values))
            if numeric(mapped_properties[0][1]):
                mean = sum(list(map(lambda x: x[1], mapped_properties)))
                blended_additional_properties.append(
                    AdditionalProperty(name=mapped_properties[0][0], value=str(round(mean, 2))))
            else:
                for item in mapped_properties:
                    blended_property_names = [x.name for x in blended_additional_properties]
                    if item[1] in blended_property_names:
                        index_of_matching_name = blended_property_names.index(item[1])
                        updated_value = float(blended_additional_properties[index_of_matching_name].value) + item[2]
                        blended_additional_properties[index_of_matching_name].value = str(round(updated_value, 2))
                    else:
                        blended_additional_properties.append(
                            AdditionalProperty(name=item[1], value=str(round(item[2], 2))))
        return blended_additional_properties

    @classmethod
    def _compute_weighted_properties_with_ratios(cls, ratio, property):
        return property.name, cls._map_according_to_value(ratio, property.value), ratio

    @classmethod
    def _map_according_to_value(cls, ratio, value):
        if numeric(value):
            return ratio * string_to_number(value)
        return value

    # we throw away all properties with keys (names) either not contained in additional_properties of all base materials
    # or if the key is contained in additional_properties of all base materials but the types of the values are not
    # matching as otherwise we cannot clearly separate continuous from categorical variables
    @classmethod
    def _keep_matching(cls, first_property_list, second_property_list):
        return [x for x in first_property_list if
                cls._is_contained_and_has_same_type_in_all_materials(x, second_property_list)]

    @classmethod
    def _is_contained_and_has_same_type_in_all_materials(cls, prop, property_list):
        matching_name = False
        matching_type = False
        names_of_properties = list(map(lambda p: p.name, property_list))
        if prop.name in names_of_properties:
            matching_name = True
        if matching_name:
            for additional_property in property_list:
                if additional_property.name == prop.name:
                    if (numeric(additional_property.value) and not_numeric(prop.value)) or (
                            not_numeric(additional_property.value) and numeric(prop.value)):
                        matching_type = False
                    else:
                        matching_type = True
        return matching_name and matching_type
