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
        dataframe['total costs'] = dataframe.apply(lambda row: cls.compute_total_costs(row), axis=1)
        dataframe = dataframe.drop([x for x in dataframe if x.startswith('costs')], 1)
        return dataframe

    @classmethod
    def compute_total_costs(cls, row):
        cost_entries = {k: v for k, v in dict(row).items() if 'costs' in k}
        total_costs = 0
        for value in cost_entries.values():
            total_costs += value
        return total_costs
