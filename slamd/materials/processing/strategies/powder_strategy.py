from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class PowderStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        composition = Composition(
            fe3_o2=submitted_material['fe3_o2'],
            si_o2=submitted_material['si_o2'],
            al2_o3=submitted_material['al2_o3'],
            ca_o=submitted_material['ca_o'],
            mg_o=submitted_material['mg_o'],
            na2_o=submitted_material['na2_o'],
            k2_o=submitted_material['k2_o'],
            s_o3=submitted_material['s_o3'],
            ti_o2=submitted_material['ti_o2'],
            p2_o5=submitted_material['p2_o5'],
            sr_o=submitted_material['sr_o'],
            mn2_o3=submitted_material['mn2_o3']
        )

        costs = Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

        structure = Structure()
        structure.gravity = submitted_material['gravity']
        structure.fine = submitted_material['fine']

        powder = Powder(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            composition=composition,
            structure=structure,
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('powder', powder)

    def _gather_composition_information(self, powder):
        return [self._include('Fe₂O₃', powder.composition.fe3_o2),
                self._include('SiO₂', powder.composition.si_o2),
                self._include('Al₂O₃', powder.composition.al2_o3),
                self._include('CaO', powder.composition.ca_o),
                self._include('MgO', powder.composition.mg_o),
                self._include('Na₂O', powder.composition.na2_o),
                self._include('K₂O', powder.composition.k2_o),
                self._include('SO₃', powder.composition.s_o3),
                self._include('TiO₂', powder.composition.ti_o2),
                self._include('P₂O₅', powder.composition.p2_o5),
                self._include('SrO', powder.composition.sr_o),
                self._include('Mn₂O₃', powder.composition.mn2_o3),
                self._include('Fine modules', powder.structure.fine),
                self._include('Specific gravity', powder.structure.gravity)]
