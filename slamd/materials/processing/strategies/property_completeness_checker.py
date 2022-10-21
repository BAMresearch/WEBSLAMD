from functools import reduce

from slamd.common.slamd_utils import empty, numeric, not_numeric


class PropertyCompletenessChecker:

    @classmethod
    def is_complete(cls, materials_as_dict, *keys):
        all_values = cls.collect_all_base_material_values_for_property(materials_as_dict, keys)

        empty_values = [value for value in all_values if empty(value)]

        if len(empty_values) > 0:
            return False
        return True

    @classmethod
    def is_complete_with_values_returned(cls, materials_as_dict, keys):
        all_values = cls.collect_all_base_material_values_for_property(materials_as_dict, keys)

        empty_values = [value for value in all_values if empty(value)]

        if len(empty_values) > 0:
            return False, None
        return True, all_values

    @classmethod
    def collect_all_base_material_values_for_property(cls, material_as_dict, keys):
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

    @classmethod
    def additional_properties_are_complete(cls, materials_as_dict):
        consistent_properties = cls.find_additional_properties_defined_in_all_base_materials(materials_as_dict)
        all_additional_properties = cls._collect_all_additional_properties(materials_as_dict)

        sizes_of_additional_properties_for_materials = [len(ps) for ps in all_additional_properties]

        if len(sizes_of_additional_properties_for_materials) == 0:
            if len(consistent_properties) == 0:
                return True
            return False
        max_number_of_props = max(sizes_of_additional_properties_for_materials)
        return max_number_of_props == len(consistent_properties)

    @classmethod
    def find_additional_properties_defined_in_all_base_materials(cls, base_materials_as_dict):
        additional_properties_for_all_base_materials = cls._collect_all_additional_properties(base_materials_as_dict)
        properties_with_key_defined_in_all_base_materials = reduce(
            cls._keep_matching, additional_properties_for_all_base_materials)
        return properties_with_key_defined_in_all_base_materials

    @classmethod
    def _collect_all_additional_properties(cls, base_materials_as_dict):
        additional_properties_for_all_base_materials = []
        for base_powder in base_materials_as_dict:
            additional_properties_for_all_base_materials.append(base_powder['additional_properties'])
        return additional_properties_for_all_base_materials

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
        names_of_properties = [prop.name for prop in property_list]
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
