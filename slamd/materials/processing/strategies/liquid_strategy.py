from dataclasses import fields

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class LiquidStrategy(MaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            na2_si_o3=float_if_not_empty(submitted_material['na2_si_o3']),
            na_o_h=float_if_not_empty(submitted_material['na_o_h']),
            na2_si_o3_specific=float_if_not_empty(submitted_material['na2_si_o3_specific']),
            na_o_h_specific=float_if_not_empty(submitted_material['na_o_h_specific']),
            total=float_if_not_empty(submitted_material['total']),
            na2_o=float_if_not_empty(submitted_material['na2_o']),
            si_o2=float_if_not_empty(submitted_material['si_o2']),
            h2_o=float_if_not_empty(submitted_material['h2_o']),
            na2_o_dry=float_if_not_empty(submitted_material['na2_o_dry']),
            si_o2_dry=float_if_not_empty(submitted_material['si_o2_dry']),
            water=float_if_not_empty(submitted_material['water']),
            na_o_h_total=float_if_not_empty(submitted_material['na_o_h_total'])
        )

        return Liquid(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def create_blended_material(cls, idx, blended_material_name, normalized_ratios, base_liquid_as_dict):
        costs = cls.compute_blended_costs(normalized_ratios, base_liquid_as_dict)
        composition = cls._compute_blended_composition(normalized_ratios, base_liquid_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_liquid_as_dict)

        return Liquid(type=base_liquid_as_dict[0]['type'],
                      name=f'{blended_material_name}-{idx}',
                      costs=costs,
                      composition=composition,
                      additional_properties=additional_properties,
                      is_blended=True,
                      blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios),
                      created_from=cls.created_from(base_liquid_as_dict))

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)
        composition_complete = cls._check_completeness_of_composition(base_materials_as_dict)

        return costs_complete and additional_properties_complete and composition_complete

    @classmethod
    def _check_completeness_of_composition(cls, base_materials_as_dict):
        pcc = PropertyCompletenessChecker

        na2_si_o3_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_si_o3')
        na_o_h_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na_o_h')
        na2_si_o3_specific_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_si_o3_specific')
        na_o_h_specific_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na_o_h_specific')
        total_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'total')
        h2_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'h2_o')
        na2_o_dry_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_o_dry')
        si_o2_dry_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'si_o2_dry')
        water_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'water')
        na_o_h_total_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na_o_h_total')

        return na2_si_o3_complete and na_o_h_complete and na2_si_o3_specific_complete and na_o_h_specific_complete \
               and total_complete and h2_o_complete and na2_o_dry_complete and si_o2_dry_complete and water_complete \
               and na_o_h_total_complete

    @classmethod
    def gather_composition_information(cls, liquid):
        return [cls.include('Na₂SiO₃', liquid.composition.na2_si_o3),
                cls.include('NaOH', liquid.composition.na_o_h),
                cls.include('Na₂SiO₃ specific', liquid.composition.na2_si_o3_specific),
                cls.include('NaOH specific', liquid.composition.na_o_h_specific),
                cls.include('Total solution', liquid.composition.total),
                cls.include('Na₂O', liquid.composition.na2_o),
                cls.include('SiO₂', liquid.composition.si_o2),
                cls.include('H₂O', liquid.composition.h2_o),
                cls.include('Na₂O', liquid.composition.na2_o_dry),
                cls.include('SiO₂', liquid.composition.si_o2_dry),
                cls.include('Water', liquid.composition.water),
                cls.include('Total NaOH', liquid.composition.na_o_h_total)]

    @classmethod
    def convert_to_multidict(cls, liquid):
        multidict = super().convert_to_multidict(liquid)
        # Iterate over the fields of Composition and convert them to string
        for field in fields(liquid.composition):
            field_value = str_if_not_none(getattr(liquid.composition, field.name))
            multidict.add(field.name, field_value)
        return multidict

    @classmethod
    def _compute_blended_composition(cls, ratios, base_liquids_as_dict):
        bpc = BlendingPropertiesCalculator

        blended_na2_si_o3 = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_si_o3')
        blended_na_o_h = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na_o_h')
        blended_na2_si_o3_specific = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_si_o3_specific')
        blended_na_o_h_specific = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na_o_h_specific')
        blended_total = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'total')
        blended_na2_o = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_o')
        blended_si_o2 = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'si_o2')
        blended_h2_o = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'h2_o')
        blended_na2_o_dry = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_o_dry')
        blended_si_o2_dry = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'si_o2_dry')
        blended_water = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'water')
        blended_na_o_h_total = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na_o_h_total')

        composition = Composition(na2_si_o3=blended_na2_si_o3, na_o_h=blended_na_o_h,
                                  na2_si_o3_specific=blended_na2_si_o3_specific,
                                  na_o_h_specific=blended_na_o_h_specific, total=blended_total, na2_o=blended_na2_o,
                                  si_o2=blended_si_o2, h2_o=blended_h2_o, na2_o_dry=blended_na2_o_dry,
                                  si_o2_dry=blended_si_o2_dry, water=blended_water, na_o_h_total=blended_na_o_h_total)

        return composition

    @classmethod
    def for_formulation(cls, material):
        pass
