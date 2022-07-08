from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AggregatesStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        composition = Composition(
            fine_aggregates=submitted_material['fine_aggregates'],
            coarse_aggregates=submitted_material['coarse_aggregates'],
            fa_density=submitted_material['fa_density'],
            ca_density=submitted_material['ca_density']
        )

        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        aggregates = Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            composition=composition,
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('aggregates', aggregates)

    def _gather_composition_information(self, aggregates):
        return [self._include('Fine Aggregates', aggregates.composition.fine_aggregates),
                self._include('Coarse Aggregates',
                              aggregates.composition.coarse_aggregates),
                self._include('FA Density', aggregates.composition.fa_density),
                self._include('CA Density', aggregates.composition.ca_density)]
