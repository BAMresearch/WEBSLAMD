from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.base_material_strategy import MaterialStrategy


class LiquidStrategy(MaterialStrategy):

    def create_model(self, submitted_material):
        composition = Composition(
            na2_si_o3=submitted_material['na2_si_o3'],
            na_o_h=submitted_material['na_o_h'],
            na2_si_o3_specific=submitted_material['na2_si_o3_specific'],
            na_o_h_specific=submitted_material['na_o_h_specific'],
            total=submitted_material['total'],
            na2_o=submitted_material['na2_o'],
            si_o2=submitted_material['si_o2'],
            h2_o=submitted_material['h2_o'],
            na2_o_dry=submitted_material['na2_o_dry'],
            si_o2_dry=submitted_material['si_o2_dry'],
            water=submitted_material['water'],
            na_o_h_total=submitted_material['na_o_h_total']
        )

        return Liquid(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def create_blended_material(self, idx, blended_material_name, normalized_ratios, base_powders_as_dict):
        costs = self.compute_blended_costs(normalized_ratios, base_powders_as_dict)
        composition = self._compute_blended_composition(normalized_ratios, base_powders_as_dict)

        return Liquid(type=base_powders_as_dict[0]['type'],
                      name=f'{blended_material_name}-{idx}',
                      costs=costs,
                      composition=composition,
                      additional_properties=[],
                      is_blended=True,
                      blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios))

    def gather_composition_information(self, liquid):
        return [self.include('Na₂SiO₃', liquid.composition.na2_si_o3),
                self.include('NaOH', liquid.composition.na_o_h),
                self.include('Na₂SiO₃ specific', liquid.composition.na2_si_o3_specific),
                self.include('NaOH specific', liquid.composition.na_o_h_specific),
                self.include('Total solution', liquid.composition.total),
                self.include('Na₂O', liquid.composition.na2_o),
                self.include('SiO₂', liquid.composition.si_o2),
                self.include('H₂O', liquid.composition.h2_o),
                self.include('Na₂O', liquid.composition.na2_o_dry),
                self.include('SiO₂', liquid.composition.si_o2_dry),
                self.include('Water', liquid.composition.water),
                self.include('Total NaOH', liquid.composition.na_o_h_total)]

    def convert_to_multidict(self, liquid):
        multidict = super().convert_to_multidict(liquid)
        multidict.add('na2_si_o3', liquid.composition.na2_si_o3)
        multidict.add('na_o_h', liquid.composition.na_o_h)
        multidict.add('na2_si_o3_specific', liquid.composition.na2_si_o3_specific)
        multidict.add('na_o_h_specific', liquid.composition.na_o_h_specific)
        multidict.add('total', liquid.composition.total)
        multidict.add('na2_o', liquid.composition.na2_o)
        multidict.add('si_o2', liquid.composition.si_o2)
        multidict.add('h2_o', liquid.composition.h2_o)
        multidict.add('na2_o_dry', liquid.composition.na2_o_dry)
        multidict.add('si_o2_dry', liquid.composition.si_o2_dry)
        multidict.add('water', liquid.composition.water)
        multidict.add('na_o_h_total', liquid.composition.na_o_h_total)
        return multidict

    def _compute_blended_composition(self, normalized_ratios, base_powders_as_dict):
        blended_na2_si_o3 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na2_si_o3')
        blended_na_o_h = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na_o_h')
        blended_na2_si_o3_specific = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition',
                                                       'na2_si_o3_specific')
        blended_na_o_h_specific = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition',
                                                    'na_o_h_specific')
        blended_total = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'total')
        blended_na2_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na2_o')
        blended_si_o2 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'si_o2')
        blended_h2_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'h2_o')
        blended_na2_o_dry = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na2_o_dry')
        blended_si_o2_dry = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'si_o2_dry')
        blended_water = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'water')
        blended_na_o_h_total = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na_o_h_total')

        composition = Composition(na2_si_o3=blended_na2_si_o3, na_o_h=blended_na_o_h,
                                  na2_si_o3_specific=blended_na2_si_o3_specific,
                                  na_o_h_specific=blended_na_o_h_specific, total=blended_total, na2_o=blended_na2_o,
                                  si_o2=blended_si_o2, h2_o=blended_h2_o, na2_o_dry=blended_na2_o_dry,
                                  si_o2_dry=blended_si_o2_dry, water=blended_water, na_o_h_total=blended_na_o_h_total)

        return composition
