from dataclasses import fields

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class AggregatesStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            fine_aggregates=float_if_not_empty(submitted_material['fine_aggregates']),
            coarse_aggregates=float_if_not_empty(submitted_material['coarse_aggregates']),
            fa_density=float_if_not_empty(submitted_material['fa_density']),
            ca_density=float_if_not_empty(submitted_material['ca_density'])
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
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)
        composition_complete = cls._check_completeness_of_composition(base_materials_as_dict)

        return costs_complete and additional_properties_complete and composition_complete

    @classmethod
    def _check_completeness_of_composition(cls, base_materials_as_dict):
        pcc = PropertyCompletenessChecker

        fine_aggregates_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'fine_aggregates')
        coarse_aggregates_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'coarse_aggregates')
        fa_density_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'fa_density')
        ca_density_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'ca_density')

        return fine_aggregates_complete and coarse_aggregates_complete and fa_density_complete and \
               ca_density_complete

    @classmethod
    def convert_to_multidict(cls, aggregates):
        multidict = super().convert_to_multidict(aggregates)
        # Iterate over the fields of Composition and convert them to string
        for field in fields(aggregates.composition):
            field_value = str_if_not_none(getattr(aggregates.composition, field.name))
            multidict.add(field.name, field_value)
        return multidict

    @classmethod
    def create_blended_material(cls, idx, blended_material_name, normalized_ratios, base_aggregates_as_dict):
        costs = cls.compute_blended_costs(normalized_ratios, base_aggregates_as_dict)
        composition = cls._compute_blended_composition(normalized_ratios, base_aggregates_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_aggregates_as_dict)

        return Aggregates(type=base_aggregates_as_dict[0]['type'],
                          name=f'{blended_material_name}-{idx}',
                          costs=costs,
                          composition=composition,
                          additional_properties=additional_properties,
                          is_blended=True,
                          blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios),
                          created_from=cls.created_from(base_aggregates_as_dict))

    @classmethod
    def _compute_blended_composition(cls, normalized_ratios, base_aggregates_as_dict):
        bpc = BlendingPropertiesCalculator

        blended_fine_aggregates = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition',
                                                   'fine_aggregates')
        blended_coarse_aggregates = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition',
                                                     'coarse_aggregates')
        blended_fa_density = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition', 'fa_density')
        blended_ca_density = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition', 'ca_density')

        composition = Composition(fine_aggregates=blended_fine_aggregates, coarse_aggregates=blended_coarse_aggregates,
                                  fa_density=blended_fa_density, ca_density=blended_ca_density)

        return composition

    @classmethod
    def for_formulation(cls, material):
        pass
