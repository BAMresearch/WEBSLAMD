from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.constants.material_constants import CUSTOM_DEFAULT_SPECIFIC_GRAVITY

class CustomStrategy(MaterialStrategy):

    @classmethod
    def create_material_from_dict(cls, dictionary):
        # Required for backwards compatibility with saved sessions from before 2025-02
        if "specific_gravity" not in dictionary:
            dictionary["specific_gravity"] = CUSTOM_DEFAULT_SPECIFIC_GRAVITY
        if dictionary["costs"] is not None and "recyclingrate" not in dictionary["costs"]:
            dictionary["costs"]["recyclingrate"] = None

        mat = Custom()
        cls.fill_material_object_with_basic_info_from_dict(mat, dictionary)
        return mat

    @classmethod
    def create_model(cls, submitted_material):
        return Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            specific_gravity=submitted_material.get('specific_gravity', CUSTOM_DEFAULT_SPECIFIC_GRAVITY),
            costs=cls.extract_cost_properties(submitted_material),
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_customs_as_dict):
        specific_gravity = cls.compute_blended_specific_gravity(normalized_ratios, base_customs_as_dict)
        costs = cls.compute_blended_costs(normalized_ratios, base_customs_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_customs_as_dict)

        return Custom(type=base_customs_as_dict[0]['type'],
                      name=name,
                      specific_gravity=specific_gravity,
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
