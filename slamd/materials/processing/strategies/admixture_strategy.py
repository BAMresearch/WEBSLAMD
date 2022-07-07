from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AdmixtureStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        admixture = Admixture()

        admixture.name = submitted_material['material_name']
        admixture.type = submitted_material['material_type']
        admixture.composition = submitted_material['composition']
        admixture.type = submitted_material['type']
        admixture.additional_properties = additional_properties
        admixture.costs = costs

        MaterialsPersistence.save('admixture', admixture)

    def _gather_composition_information(self, admixture):
        return [self._include('Composition', admixture.composition),
                self._include('Type', admixture.type)]
