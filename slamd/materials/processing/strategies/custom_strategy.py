from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class CustomStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            custom_name=submitted_material['custom_name'],
            custom_value=submitted_material['custom_value'],
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, custom):
        return [cls.include('Name', custom.custom_name),
                cls.include('Value', custom.custom_value)]

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)
        composition_complete = cls._check_completeness_of_composition(base_materials_as_dict)

        return costs_complete and additional_properties_complete and composition_complete

    @classmethod
    def _check_completeness_of_composition(cls, base_materials_as_dict):
        pcc = PropertyCompletenessChecker

        custom_name_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'custom_name')
        custom_value_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'custom_value')

        return custom_name_complete and custom_value_complete

    @classmethod
    def convert_to_multidict(cls, custom):
        multidict = super().convert_to_multidict(custom)
        multidict.add('custom_name', custom.custom_name)
        multidict.add('custom_value', custom.custom_value)
        return multidict
