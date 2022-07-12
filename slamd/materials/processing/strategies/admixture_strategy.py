from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AdmixtureStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        costs = Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

        admixture = Admixture(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            composition=submitted_material['composition'],
            admixture_type=submitted_material['type'],
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('admixture', admixture)

    def gather_composition_information(self, admixture):
        return [self.include('Composition', admixture.composition),
                self.include('Type', admixture.admixture_type)]
