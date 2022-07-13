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

        aggregates = Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=additional_properties
        )

        self.save_material(aggregates)

    def gather_composition_information(self, aggregates):
        return [self.include('Fine Aggregates', aggregates.composition.fine_aggregates),
                self.include('Coarse Aggregates',
                             aggregates.composition.coarse_aggregates),
                self.include('FA Density', aggregates.composition.fa_density),
                self.include('CA Density', aggregates.composition.ca_density)]
