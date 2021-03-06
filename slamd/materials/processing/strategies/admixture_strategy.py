from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class AdmixtureStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material):
        return Admixture(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=submitted_material['composition'],
            admixture_type=submitted_material['type'],
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, admixture):
        return [self.include('Composition', admixture.composition),
                self.include('Type', admixture.admixture_type)]

    def convert_to_multidict(self, admixture):
        multidict = super().convert_to_multidict(admixture)
        multidict.add('composition', admixture.composition)
        multidict.add('type', admixture.admixture_type)
        return multidict
