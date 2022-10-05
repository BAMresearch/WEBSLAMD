from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class CustomStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_customs_as_dict):
        costs = cls.compute_blended_costs(normalized_ratios, base_customs_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_customs_as_dict)

        return Custom(type=base_customs_as_dict[0]['type'],
                      name=name,
                      costs=costs,
                      additional_properties=additional_properties,
                      is_blended=True,
                      blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios),
                      created_from=cls.created_from(base_customs_as_dict))

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)

        return costs_complete and additional_properties_complete

    @classmethod
    def convert_to_multidict(cls, custom):
        return super().convert_to_multidict(custom)

    @classmethod
    def _compute_blended_composition(cls, normalized_ratios, base_customs_as_dict):
        pass

    @classmethod
    def for_formulation(cls, custom):
        return super().for_formulation(custom)
