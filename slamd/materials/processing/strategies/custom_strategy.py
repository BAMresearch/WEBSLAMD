from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class CustomStrategy(BaseMaterialStrategy):

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
    def convert_to_multidict(cls, custom):
        multidict = super().convert_to_multidict(custom)
        multidict.add('name', custom.custom_name)
        multidict.add('value', custom.custom_value)
        return multidict
