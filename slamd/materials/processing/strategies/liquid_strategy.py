from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class LiquidStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
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

        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        liquid = Liquid(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            composition=composition,
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('liquid', liquid)

    def _gather_composition_information(self, liquid):
        return [self._include('Na₂SiO₃', liquid.composition.na2_si_o3),
                self._include('NaOH', liquid.composition.na_o_h),
                self._include('Na₂SiO₃ specific',
                              liquid.composition.na2_si_o3_specific),
                self._include('NaOH specific',
                              liquid.composition.na_o_h_specific),
                self._include('Total solution', liquid.composition.total),
                self._include('Na₂O', liquid.composition.na2_o),
                self._include('SiO₂', liquid.composition.si_o2),
                self._include('H₂O', liquid.composition.h2_o),
                self._include('Na₂O', liquid.composition.na2_o_dry),
                self._include('SiO₂', liquid.composition.si_o2_dry),
                self._include('Water', liquid.composition.water),
                self._include('Total NaOH', liquid.composition.na_o_h_total)]
