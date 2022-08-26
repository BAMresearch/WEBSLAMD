from slamd.common.slamd_utils import not_empty
from slamd.materials.processing.materials_facade import MaterialsFacade
import pandas as pd


class FormulationsConverter:
    """
    The parameter material_combinations is a list of tuples where each element in the list represents a variation of one
    of the materials for a given type. E.g. if two powders P1 and P2, one liquid L and one aggregate A were chosen,
    this list would contain two elements [(P1, L, A), (P2, L, A)]
    """

    @classmethod
    def formulation_to_df(cls, material_combinations, processes, weight_data):
        all_rows = []
        for material_combination in material_combinations:
            full_dict, types = MaterialsFacade.materials_formulation_as_dict(material_combination, processes)
            original_dict = full_dict.copy()

            for weights in weight_data:
                weight_dict = {}
                for i, weight in enumerate(weights.split('/')):
                    weight_dict[f'{types[i]} (kg)'] = weight
                    costs_for_type = full_dict.get(f'costs ({types[i]})', None)

                    if costs_for_type:
                        full_dict[f'costs ({types[i]})'] = full_dict[f'costs ({types[i]})'] * float(weight)

                    co2_footprint_for_type = full_dict.get(f'co2_footprint ({types[i]})', None)
                    if co2_footprint_for_type:
                        full_dict[f'co2_footprint ({types[i]})'] = full_dict[f'co2_footprint ({types[i]})'] * float(weight)

                all_rows.append({**weight_dict, **full_dict})
                full_dict = original_dict.copy()
        dataframe = pd.DataFrame(all_rows)
        dataframe['total costs'] = dataframe.apply(lambda row: cls._compute_sum(row, 'costs'), axis=1)
        dataframe['total co2_footprint'] = dataframe.apply(lambda row: cls._compute_sum(row, 'co2_footprint'), axis=1)
        dataframe['total delivery_time '] = dataframe.apply(lambda row: cls._compute_max(row), axis=1)
        dataframe = dataframe.loc[:, ~dataframe.columns.str.startswith('costs')]
        dataframe = dataframe.loc[:, ~dataframe.columns.str.startswith('co2_footprint')]
        dataframe = dataframe.loc[:, ~dataframe.columns.str.startswith('delivery_time')]
        return dataframe

    @classmethod
    def _compute_sum(cls, row, property_name):
        entries_for_property_name = {k: v for k, v in dict(row).items() if property_name in k}
        total_costs = 0
        for value in entries_for_property_name.values():
            total_costs += value
        return total_costs

    @classmethod
    def _compute_max(cls, row):
        delivery_time_entries = {k: v for k, v in dict(row).items() if 'delivery_time' in k}
        max = 0
        for value in delivery_time_entries.values():
            if value > max:
                max = value
        return max
