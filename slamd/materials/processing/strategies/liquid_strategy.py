from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class LiquidStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        composition = Composition()
        composition.na2_si_o3 = submitted_material['na2_si_o3']
        composition.na_o_h = submitted_material['na_o_h']
        composition.na2_si_o3_specific = submitted_material['na2_si_o3_specific']
        composition.na_o_h_specific = submitted_material['na_o_h_specific']
        composition.total = submitted_material['total']
        composition.na2_o = submitted_material['na2_o']
        composition.si_o2 = submitted_material['si_o2']
        composition.h2_o = submitted_material['h2_o']
        composition.na2_o_dry = submitted_material['na2_o_dry']
        composition.si_o2_dry = submitted_material['si_o2_dry']
        composition.water = submitted_material['water']
        composition.na_o_h_total = submitted_material['na_o_h_total']

        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        liquid = Liquid()

        liquid.name = submitted_material['material_name']
        liquid.type = submitted_material['material_type']
        liquid.costs = costs
        liquid.composition = composition
        liquid.additional_properties = additional_properties

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