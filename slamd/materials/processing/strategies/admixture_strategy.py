from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AdmixtureStrategy(BaseMaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Admixture(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=float(submitted_material['composition']),
            admixture_type=submitted_material['type'],
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, admixture):
        return [cls.include('Composition', admixture.composition),
                cls.include('Type', admixture.admixture_type)]

    @classmethod
    def convert_to_multidict(cls, admixture):
        multidict = super().convert_to_multidict(admixture)
        multidict.add('composition', admixture.composition)
        multidict.add('type', admixture.admixture_type)
        return multidict
