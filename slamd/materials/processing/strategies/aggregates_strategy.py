from dataclasses import fields, asdict

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none, write_dict_into_object
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker
from slamd.materials.processing.constants.material_constants import AGGREGATE_DEFAULT_DENSITY

KEY_COMPOSITION = 'composition'


class AggregatesStrategy(MaterialStrategy):

    @classmethod
    def convert_material_to_dict(cls, material):
        out = super().convert_material_to_dict(material)
        if material.composition:
            out[KEY_COMPOSITION] = asdict(material.composition)

        return out

    @classmethod
    def create_material_from_dict(cls, dictionary):
        aggregates = Aggregates()
        cls.fill_material_object_with_basic_info_from_dict(aggregates, dictionary)

        if dictionary[KEY_COMPOSITION]:
            new_composition = Composition()
            write_dict_into_object(dictionary[KEY_COMPOSITION], new_composition)
            aggregates.composition = new_composition

        return aggregates

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            fine_aggregates=float_if_not_empty(submitted_material.get('fine_aggregates', None)),
            coarse_aggregates=float_if_not_empty(submitted_material.get('coarse_aggregates', None)),
            gravity=float_if_not_empty(submitted_material.get('gravity', None)),
            fineness_modulus=float_if_not_empty(submitted_material.get('fineness_modulus', None)),
            water_absorption=float_if_not_empty(submitted_material.get('water_absorption', None))
        )

        return Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            density=submitted_material.get('density', AGGREGATE_DEFAULT_DENSITY),
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, aggregates):
        return [cls.include('Fine Aggregates (m%)', aggregates.composition.fine_aggregates),
                cls.include('Coarse Aggregates (m%)', aggregates.composition.coarse_aggregates),
                cls.include('Specific Gravity', aggregates.composition.gravity),
                cls.include('Fineness modulus (m³/kg)', aggregates.composition.fineness_modulus),
                cls.include('Water absorption (m%)', aggregates.composition.water_absorption)]

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
        gravity_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'gravity')
        fineness_modulus_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'fineness_modulus')
        water_absorption_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'water_absorption')

        return (fine_aggregates_complete and coarse_aggregates_complete and gravity_complete and
                fineness_modulus_complete and water_absorption_complete)

    @classmethod
    def convert_to_multidict(cls, aggregates):
        multidict = super().convert_to_multidict(aggregates)
        # Iterate over the fields of Composition and convert them to string
        for field in fields(aggregates.composition):
            field_value = str_if_not_none(getattr(aggregates.composition, field.name))
            multidict.add(field.name, field_value)
        return multidict

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_aggregates_as_dict):
        density = cls.compute_blended_density(normalized_ratios, base_aggregates_as_dict)
        costs = cls.compute_blended_costs(normalized_ratios, base_aggregates_as_dict)
        composition = cls._compute_blended_composition(normalized_ratios, base_aggregates_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_aggregates_as_dict)

        return Aggregates(type=base_aggregates_as_dict[0]['type'],
                          name=name,
                          density=density,
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
        blended_gravity = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition', 'gravity')

        blended_fineness_modulus = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition',
                                                    'fineness_modulus')
        blended_water_absorption = bpc.compute_mean(normalized_ratios, base_aggregates_as_dict, 'composition',
                                                    'water_absorption')

        composition = Composition(fine_aggregates=blended_fine_aggregates, coarse_aggregates=blended_coarse_aggregates,
                                  gravity=blended_gravity, fineness_modulus=blended_fineness_modulus,
                                  water_absorption=blended_water_absorption)

        return composition

    @classmethod
    def for_formulation(cls, aggregates):
        multidict = super().for_formulation(aggregates)
        for field in fields(aggregates.composition):
            field_value = float_if_not_empty(getattr(aggregates.composition, field.name))
            multidict.add(field.name, field_value)
        return multidict
