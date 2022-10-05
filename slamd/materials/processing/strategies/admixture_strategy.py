from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class AdmixtureStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Admixture(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)

        return costs_complete and additional_properties_complete

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_admixtures_as_dict):
        costs = cls.compute_blended_costs(normalized_ratios, base_admixtures_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_admixtures_as_dict)

        return Admixture(type=base_admixtures_as_dict[0]['type'],
                         name=name,
                         costs=costs,
                         additional_properties=additional_properties,
                         is_blended=True,
                         blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios))

    @classmethod
    def convert_to_multidict(cls, admixture):
        return super().convert_to_multidict(admixture)

    @classmethod
    def for_formulation(cls, admixture):
        return super().for_formulation(admixture)
