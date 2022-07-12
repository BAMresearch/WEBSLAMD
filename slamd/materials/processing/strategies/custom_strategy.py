from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class CustomStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        custom = Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_costs_properties(submitted_material),
            custom_name=submitted_material['name'],
            custom_value=submitted_material['value'],
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('custom', custom)

    def gather_composition_information(self, custom):
        return [self.include('Name', custom.custom_name),
                self.include('Value', custom.custom_value)]
