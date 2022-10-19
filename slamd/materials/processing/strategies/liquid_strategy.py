from dataclasses import fields, asdict

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none, write_dict_into_object
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker

KEY_COMPOSITION = 'composition'


class LiquidStrategy(MaterialStrategy):

    @classmethod
    def convert_material_to_dict(cls, material):
        out = super().convert_material_to_dict(material)
        if material.composition:
            out[KEY_COMPOSITION] = asdict(material.composition)

        return out

    @classmethod
    def create_material_from_dict(cls, dictionary):
        liquid = Liquid()
        cls.fill_material_object_with_basic_info_from_dict(liquid, dictionary)

        if dictionary[KEY_COMPOSITION]:
            new_composition = Composition()
            write_dict_into_object(dictionary[KEY_COMPOSITION], new_composition)
            liquid.composition = new_composition

        return liquid

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            na2_si_o3=float_if_not_empty(submitted_material['na2_si_o3']),
            na_o_h=float_if_not_empty(submitted_material['na_o_h']),
            na2_si_o3_mol=float_if_not_empty(submitted_material['na2_si_o3_mol']),
            na_o_h_mol=float_if_not_empty(submitted_material['na_o_h_mol']),
            na2_o=float_if_not_empty(submitted_material['na2_o']),
            si_o2=float_if_not_empty(submitted_material['si_o2']),
            h2_o=float_if_not_empty(submitted_material['h2_o']),
            na2_o_mol=float_if_not_empty(submitted_material['na2_o_mol']),
            si_o2_mol=float_if_not_empty(submitted_material['si_o2_mol']),
            h2_o_mol=float_if_not_empty(submitted_material['h2_o_mol'])
        )

        return Liquid(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_liquid_as_dict):
        costs = cls.compute_blended_costs(normalized_ratios, base_liquid_as_dict)
        composition = cls._compute_blended_composition(normalized_ratios, base_liquid_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_liquid_as_dict)

        return Liquid(type=base_liquid_as_dict[0]['type'],
                      name=name,
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
        na2_si_o3_mol_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_si_o3_mol')
        na_o_h_mol_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na_o_h_mol')
        h2_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'h2_o')
        na2_o_mol_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_o_mol')
        si_o2_mol_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'si_o2_mol')
        h2_o_mol_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'h2_o_mol')

        return na2_si_o3_complete and na_o_h_complete and na2_si_o3_mol_complete and na_o_h_mol_complete \
               and h2_o_complete and na2_o_mol_complete and si_o2_mol_complete and h2_o_mol_complete

    @classmethod
    def gather_composition_information(cls, liquid):
        return [cls.include('Na₂SiO₃ (m%)', liquid.composition.na2_si_o3),
                cls.include('Na₂SiO₃ (mol%)', liquid.composition.na2_si_o3_mol),
                cls.include('NaOH (m%)', liquid.composition.na_o_h),
                cls.include('NaOH (mol%)', liquid.composition.na_o_h_mol),
                cls.include('Na₂O (m%)', liquid.composition.na2_o),
                cls.include('Na₂O (mol%)', liquid.composition.na2_o_mol),
                cls.include('SiO₂ (m%)', liquid.composition.si_o2),
                cls.include('SiO₂ (mol%)', liquid.composition.si_o2_mol),
                cls.include('H₂O (m%)', liquid.composition.h2_o),
                cls.include('H₂O (mol%)', liquid.composition.h2_o_mol)]

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
        blended_na2_si_o3_mol = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_si_o3_mol')
        blended_na_o_h_mol = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na_o_h_mol')
        blended_na2_o = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_o')
        blended_si_o2 = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'si_o2')
        blended_h2_o = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'h2_o')
        blended_na2_o_mol = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'na2_o_mol')
        blended_si_o2_mol = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'si_o2_mol')
        blended_h2_o_mol = bpc.compute_mean(ratios, base_liquids_as_dict, 'composition', 'h2_o_mol')

        composition = Composition(na2_si_o3=blended_na2_si_o3, na_o_h=blended_na_o_h,
                                  na2_si_o3_mol=blended_na2_si_o3_mol,
                                  na_o_h_mol=blended_na_o_h_mol, na2_o=blended_na2_o,
                                  si_o2=blended_si_o2, h2_o=blended_h2_o, na2_o_mol=blended_na2_o_mol,
                                  si_o2_mol=blended_si_o2_mol, h2_o_mol=blended_h2_o_mol)

        return composition

    @classmethod
    def for_formulation(cls, liquid):
        multidict = super().for_formulation(liquid)
        for field in fields(liquid.composition):
            field_value = float_if_not_empty(getattr(liquid.composition, field.name))
            multidict.add(field.name, field_value)
        return multidict
