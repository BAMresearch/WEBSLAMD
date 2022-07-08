from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class CustomStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        costs = Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

        custom = Custom(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            custom_name=submitted_material['name'],
            custom_value=submitted_material['value'],
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('custom', custom)

    def _gather_composition_information(self, custom):
        return [self._include('Name', custom.custom_name),
                self._include('Value', custom.custom_value)]
