from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AggregatesStrategy(BaseMaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            fine_aggregates=float_if_not_empty(submitted_material['fine_aggregates']),
            coarse_aggregates=float_if_not_empty(submitted_material['coarse_aggregates']),
            fa_density=submitted_material['fa_density'],
            ca_density=submitted_material['ca_density']
        )

        return Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, aggregates):
        return [cls.include('Fine Aggregates', aggregates.composition.fine_aggregates),
                cls.include('Coarse Aggregates', aggregates.composition.coarse_aggregates),
                cls.include('FA Density', aggregates.composition.fa_density),
                cls.include('CA Density', aggregates.composition.ca_density)]

    @classmethod
    def convert_to_multidict(cls, aggregates):
        multidict = super().convert_to_multidict(aggregates)
        multidict.add('fine_aggregates', str_if_not_none(aggregates.composition.fine_aggregates))
        multidict.add('coarse_aggregates', str_if_not_none(aggregates.composition.coarse_aggregates))
        multidict.add('fa_density', aggregates.composition.fa_density)
        multidict.add('ca_density', aggregates.composition.ca_density)
        return multidict
