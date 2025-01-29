from dataclasses import fields, asdict
from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none, write_dict_into_object
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker
from slamd.materials.processing.constants.material_constants import POWDER_DEFAULT_SPECIFIC_GRAVITY

KEY_COMPOSITION = 'composition'
KEY_STRUCTURE = 'structure'


class PowderStrategy(MaterialStrategy):

    @classmethod
    def convert_material_to_dict(cls, material):
        out = super().convert_material_to_dict(material)

        if material.composition:
            out[KEY_COMPOSITION] = asdict(material.composition)
        if material.structure:
            out[KEY_STRUCTURE] = asdict(material.structure)

        return out

    @classmethod
    def create_material_from_dict(cls, dictionary):
        powder = Powder()
        cls.fill_material_object_with_basic_info_from_dict(powder, dictionary)

        if dictionary[KEY_COMPOSITION]:
            new_composition = Composition()
            write_dict_into_object(dictionary[KEY_COMPOSITION], new_composition)
            powder.composition = new_composition

        if dictionary[KEY_STRUCTURE]:
            new_structure = Structure()
            write_dict_into_object(dictionary[KEY_STRUCTURE], new_structure)
            powder.structure = new_structure

        return powder

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            fe3_o2=float_if_not_empty(submitted_material.get('fe3_o2', None)),
            si_o2=float_if_not_empty(submitted_material.get('si_o2', None)),
            al2_o3=float_if_not_empty(submitted_material.get('al2_o3', None)),
            ca_o=float_if_not_empty(submitted_material.get('ca_o', None)),
            mg_o=float_if_not_empty(submitted_material.get('mg_o', None)),
            na2_o=float_if_not_empty(submitted_material.get('na2_o', None)),
            k2_o=float_if_not_empty(submitted_material.get('k2_o', None)),
            s_o3=float_if_not_empty(submitted_material.get('s_o3', None)),
            ti_o2=float_if_not_empty(submitted_material.get('ti_o2', None)),
            p2_o5=float_if_not_empty(submitted_material.get('p2_o5', None)),
            sr_o=float_if_not_empty(submitted_material.get('sr_o', None)),
            mn2_o3=float_if_not_empty(submitted_material.get('mn2_o3', None)),
            loi=float_if_not_empty(submitted_material.get('loi', None))
        )

        structure = Structure(
            fine=float_if_not_empty(submitted_material.get('fine', None))
        )
        return Powder(
            name=submitted_material.get('material_name', None),
            type=submitted_material.get('material_type', None),
            specific_gravity=submitted_material.get('specific_gravity', POWDER_DEFAULT_SPECIFIC_GRAVITY),
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            structure=structure,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, powder):
        return [cls.include('Fe₂O₃ (m%)', powder.composition.fe3_o2),
                cls.include('SiO₂ (m%)', powder.composition.si_o2),
                cls.include('Al₂O₃ (m%)', powder.composition.al2_o3),
                cls.include('CaO (m%)', powder.composition.ca_o),
                cls.include('MgO (m%)', powder.composition.mg_o),
                cls.include('Na₂O (m%)', powder.composition.na2_o),
                cls.include('K₂O (m%)', powder.composition.k2_o),
                cls.include('SO₃ (m%)', powder.composition.s_o3),
                cls.include('TiO₂ (m%)', powder.composition.ti_o2),
                cls.include('P₂O₅ (m%)', powder.composition.p2_o5),
                cls.include('SrO (m%)', powder.composition.sr_o),
                cls.include('Mn₂O₃ (m%)', powder.composition.mn2_o3),
                cls.include('LOI (m%)', powder.composition.loi),
                cls.include('Fine modules (m²/kg)', powder.structure.fine)]

    @classmethod
    def convert_to_multidict(cls, powder):
        multidict = super().convert_to_multidict(powder)
        # Iterate over the fields of Composition and convert them to string
        for field in fields(powder.composition):
            field_value = str_if_not_none(getattr(powder.composition, field.name))
            multidict.add(field.name, field_value)
        multidict.add('fine', str_if_not_none(powder.structure.fine))
        return multidict

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_powders_as_dict):
        specific_gravity = cls.compute_blended_specific_gravity(normalized_ratios, base_powders_as_dict)
        costs = cls.compute_blended_costs(normalized_ratios, base_powders_as_dict)
        composition = cls._compute_blended_composition(normalized_ratios, base_powders_as_dict)
        structure = cls._compute_blended_structure(normalized_ratios, base_powders_as_dict)
        additional_properties = cls.compute_additional_properties(normalized_ratios, base_powders_as_dict)

        return Powder(type=base_powders_as_dict[0]['type'],
                      name=name,
                      specific_gravity=specific_gravity,
                      costs=costs,
                      composition=composition,
                      structure=structure,
                      additional_properties=additional_properties,
                      is_blended=True,
                      blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios),
                      created_from=cls.created_from(base_powders_as_dict))

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        costs_complete = cls.check_completeness_of_costs(base_materials_as_dict)
        additional_properties_complete = cls.check_completeness_of_additional_properties(base_materials_as_dict)
        composition_complete = cls._check_completeness_of_composition(base_materials_as_dict)
        structure_complete = cls._check_completeness_of_structure(base_materials_as_dict)

        return costs_complete and additional_properties_complete and composition_complete and structure_complete

    @classmethod
    def _check_completeness_of_composition(cls, base_materials_as_dict):
        pcc = PropertyCompletenessChecker

        fe2_o3_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'fe3_o2')
        si_o2_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'si_o2')
        al2_o3_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'al2_o3')
        na2_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'na2_o')
        ca_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'ca_o')
        mg_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'mg_o')
        k2_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'k2_o')
        s_o3_complete = pcc.is_complete(base_materials_as_dict, 'composition', 's_o3')
        ti_o2_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'ti_o2')
        p2_o5_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'p2_o5')
        sr_o_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'sr_o')
        mn2_o3_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'mn2_o3')
        loi_complete = pcc.is_complete(base_materials_as_dict, 'composition', 'loi')

        return fe2_o3_complete and si_o2_complete and al2_o3_complete and na2_o_complete and ca_o_complete and \
            mg_o_complete and k2_o_complete and s_o3_complete and ti_o2_complete and p2_o5_complete and \
            sr_o_complete and mn2_o3_complete and loi_complete

    @classmethod
    def _check_completeness_of_structure(cls, base_materials_as_dict):
        fine_complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'structure', 'fine')

        return fine_complete

    @classmethod
    def _compute_blended_composition(cls, normalized_ratios, base_powders_as_dict):
        bpc = BlendingPropertiesCalculator

        blended_fe2_o3 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'fe3_o2')
        blended_si_o2 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'si_o2')
        blended_al2_o3 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'al2_o3')
        blended_na2_o = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na2_o')

        blended_ca_o = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'ca_o')
        blended_mg_o = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'mg_o')
        blended_k2_o = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'k2_o')
        blended_s_o3 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 's_o3')

        blended_ti_o2 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'ti_o2')
        blended_p2_o5 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'p2_o5')
        blended_sr_o = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'sr_o')
        blended_mn2_o3 = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'mn2_o3')
        blended_loi = bpc.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'loi')

        composition = Composition(fe3_o2=blended_fe2_o3, si_o2=blended_si_o2, al2_o3=blended_al2_o3,
                                  na2_o=blended_na2_o, ca_o=blended_ca_o, mg_o=blended_mg_o,
                                  k2_o=blended_k2_o, s_o3=blended_s_o3, ti_o2=blended_ti_o2,
                                  p2_o5=blended_p2_o5, sr_o=blended_sr_o, mn2_o3=blended_mn2_o3, loi=blended_loi)

        return composition

    @classmethod
    def _compute_blended_structure(cls, normalized_ratios, base_powders_as_dict):
        blended_fine = BlendingPropertiesCalculator.compute_mean(normalized_ratios, base_powders_as_dict, 'structure',
                                                                 'fine')

        return Structure(fine=blended_fine)

    @classmethod
    def for_formulation(cls, powder):
        multidict = super().for_formulation(powder)
        for field in fields(powder.composition):
            field_value = float_if_not_empty(getattr(powder.composition, field.name))
            multidict.add(field.name, field_value)
        multidict.add('fine', float_if_not_empty(powder.structure.fine))
        return multidict
