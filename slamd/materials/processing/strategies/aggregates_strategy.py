from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AggregatesStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material):
        composition = Composition(
            fine_aggregates=submitted_material['fine_aggregates'],
            coarse_aggregates=submitted_material['coarse_aggregates'],
            fa_density=submitted_material['fa_density'],
            ca_density=submitted_material['ca_density']
        )

        return Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, aggregates):
        return [self.include('Fine Aggregates', aggregates.composition.fine_aggregates),
                self.include('Coarse Aggregates', aggregates.composition.coarse_aggregates),
                self.include('FA Density', aggregates.composition.fa_density),
                self.include('CA Density', aggregates.composition.ca_density)]

    def convert_to_multidict(self, aggregates):
        multidict = super().convert_to_multidict(aggregates)
        multidict.add('fine_aggregates', aggregates.composition.fine_aggregates)
        multidict.add('coarse_aggregates', aggregates.composition.coarse_aggregates)
        multidict.add('fa_density', aggregates.composition.fa_density)
        multidict.add('ca_density', aggregates.composition.ca_density)
        return multidict
