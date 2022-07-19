from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class LiquidStrategy(BaseMaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        composition = Composition(
            na2_si_o3=float(submitted_material['na2_si_o3']),
            na_o_h=float(submitted_material['na_o_h']),
            na2_si_o3_specific=float(submitted_material['na2_si_o3_specific']),
            na_o_h_specific=float(submitted_material['na_o_h_specific']),
            total=float(submitted_material['total']),
            na2_o=float(submitted_material['na2_o']),
            si_o2=float(submitted_material['si_o2']),
            h2_o=float(submitted_material['h2_o']),
            na2_o_dry=float(submitted_material['na2_o_dry']),
            si_o2_dry=float(submitted_material['si_o2_dry']),
            water=float(submitted_material['water']),
            na_o_h_total=float(submitted_material['na_o_h_total'])
        )

        return Liquid(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

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
