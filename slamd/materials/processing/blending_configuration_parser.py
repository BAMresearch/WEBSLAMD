from slamd.common.slamd_utils import string_to_number


class RatioParser:

    @classmethod
    def create_list_of_normalized_ratio_lists(cls, all_ratios, delimiter):
        return list(map(lambda ratio: cls._to_normalized_ratio_list(ratio, delimiter), all_ratios))

    @classmethod
    def create_ratio_string(cls, entry):
        entry_list = list(entry)
        sum_of_independent_ratios = sum(entry_list)
        dependent_ratio_value = round(100 - sum_of_independent_ratios, 2)
        independent_ratio_values = "/".join(map(lambda entry: str(round(entry, 2)), entry_list))
        all_ratios_for_entry = f'{independent_ratio_values}/{dependent_ratio_value}'
        return all_ratios_for_entry

    @classmethod
    def _to_normalized_ratio_list(cls, ratio, delimiter):
        pieces = ratio.split(delimiter)
        ratio_list = []
        for piece in pieces:
            ratio_list.append(string_to_number(piece))
        normalized_ratio_list = list(map(lambda ratio: ratio / sum(ratio_list), ratio_list))
        return normalized_ratio_list
