from slamd.common.slamd_utils import empty


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
