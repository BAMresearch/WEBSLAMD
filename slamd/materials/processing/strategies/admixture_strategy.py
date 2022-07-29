from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class AdmixtureStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Admixture(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=float_if_not_empty(submitted_material['composition']),
            admixture_type=submitted_material['type'],
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, admixture):
        return [cls.include('Composition', admixture.composition),
                cls.include('Type', admixture.admixture_type)]

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)
        composition_complete = cls._check_completeness_of_composition(base_materials_as_dict)

        return costs_complete and additional_properties_complete and composition_complete

    @classmethod
    def _check_completeness_of_composition(cls, base_materials_as_dict):
        pcc = PropertyCompletenessChecker

        composition_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'composition')
        admixture_type_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'admixture_type')

        return composition_complete and admixture_type_complete

    @classmethod
    def convert_to_multidict(cls, admixture):
        multidict = super().convert_to_multidict(admixture)
        multidict.add('composition', str_if_not_none(admixture.composition))
        multidict.add('type', admixture.admixture_type)
        return multidict

    @classmethod
    def for_formulation(cls, admixture):
        multidict = super().for_formulation(admixture)
        multidict.add('composition', float_if_not_empty(admixture.composition))
        multidict.add('admixture type', str_if_not_none(admixture.admixture_type))
        return multidict
