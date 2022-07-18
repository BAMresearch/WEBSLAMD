from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.strategies.base_material_strategy import MaterialStrategy


class CustomStrategy(MaterialStrategy):

    def create_model(self, submitted_material):
        return Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            custom_name=submitted_material['name'],
            custom_value=submitted_material['value'],
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, custom):
        return [self.include('Name', custom.custom_name),
                self.include('Value', custom.custom_value)]

    def convert_to_multidict(self, custom):
        multidict = super().convert_to_multidict(custom)
        multidict.add('name', custom.custom_name)
        multidict.add('value', custom.custom_value)
        return multidict
