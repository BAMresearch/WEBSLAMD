from slamd.materials.materials_persistence import MaterialsPersistence
from slamd.materials.model.base_material import Costs
from slamd.materials.model.custom import Custom
from slamd.materials.strategies.base_material_strategy import BaseMaterialStrategy


class CustomStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        custom = Custom()

        custom.name = submitted_material['material_name']
        custom.type = submitted_material['material_type']
        custom.name = submitted_material['name']
        custom.value = submitted_material['value']
        custom.additional_properties = additional_properties
        custom.costs = costs

        MaterialsPersistence.save('custom', custom)

    def _gather_composition_information(self, custom):
        return [self._include('Name', custom.name),
                self._include('Vale', custom.value)]
