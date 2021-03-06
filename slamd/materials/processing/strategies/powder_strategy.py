from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class PowderStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material):
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

        structure = Structure(
            gravity=submitted_material['gravity'],
            fine=submitted_material['fine']
        )

        return Powder(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            structure=structure,
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, powder):
        return [self.include('Fe₂O₃', powder.composition.fe3_o2),
                self.include('SiO₂', powder.composition.si_o2),
                self.include('Al₂O₃', powder.composition.al2_o3),
                self.include('CaO', powder.composition.ca_o),
                self.include('MgO', powder.composition.mg_o),
                self.include('Na₂O', powder.composition.na2_o),
                self.include('K₂O', powder.composition.k2_o),
                self.include('SO₃', powder.composition.s_o3),
                self.include('TiO₂', powder.composition.ti_o2),
                self.include('P₂O₅', powder.composition.p2_o5),
                self.include('SrO', powder.composition.sr_o),
                self.include('Mn₂O₃', powder.composition.mn2_o3),
                self.include('Fine modules', powder.structure.fine),
                self.include('Specific gravity', powder.structure.gravity)]

    def convert_to_multidict(self, powder):
        multidict = super().convert_to_multidict(powder)
        multidict.add('fe3_o2', powder.composition.fe3_o2)
        multidict.add('si_o2', powder.composition.si_o2)
        multidict.add('al2_o3', powder.composition.al2_o3)
        multidict.add('ca_o', powder.composition.ca_o)
        multidict.add('mg_o', powder.composition.mg_o)
        multidict.add('na2_o', powder.composition.na2_o)
        multidict.add('k2_o', powder.composition.k2_o)
        multidict.add('s_o3', powder.composition.s_o3)
        multidict.add('ti_o2', powder.composition.ti_o2)
        multidict.add('p2_o5', powder.composition.p2_o5)
        multidict.add('sr_o', powder.composition.sr_o)
        multidict.add('mn2_o3', powder.composition.mn2_o3)
        multidict.add('fine', powder.structure.fine)
        multidict.add('gravity', powder.structure.gravity)
        return multidict
