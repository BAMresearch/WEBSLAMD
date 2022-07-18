from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import string_to_number, empty
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.ratio_parser import RatioParser
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

        structure = Structure(
            gravity=submitted_material['gravity'],
            fine=submitted_material['fine']
        )

        powder = Powder(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            structure=structure,
            additional_properties=additional_properties
        )

        self.save_material(powder)

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

    def create_blended_materials(self, blended_material_name, list_of_normalizes_ratios_lists, base_materials_as_dict):
        for i, ratio_list in enumerate(list_of_normalizes_ratios_lists):
            self.create_blended_material(i, blended_material_name, ratio_list, base_materials_as_dict)

    def create_blended_material(self, idx, blended_material_name, normalized_ratios, base_powders_as_dict):
        if len(normalized_ratios) != len(base_powders_as_dict):
            raise ValueNotSupportedException("Ratios cannot be matched with base materials!")

        blended_powder = Powder()
        blended_powder.type = base_powders_as_dict[0]['type']
        blended_powder.name = f'{blended_material_name}-{idx}'
        blended_powder.is_blended = True
        blended_powder.blending_ratios = RatioParser.ratio_list_to_ratio_string(normalized_ratios)

        self._compute_composition(blended_powder, normalized_ratios, base_powders_as_dict)

        self.save_material(blended_powder)

    def _compute_composition(self, blended_powder, normalized_ratios, base_powders_as_dict):
        blended_fe2_o3 = self._compute_mean_with_default(normalized_ratios, base_powders_as_dict, 'composition', 'fe3_o2')
        blended_si_o2 = self._compute_mean_with_default(normalized_ratios, base_powders_as_dict, 'composition', 'si_o2')
        blended_na2_o = self._compute_mean_with_default(normalized_ratios, base_powders_as_dict, 'composition', 'na2_o')
        composition = Composition(fe3_o2=blended_fe2_o3, si_o2=blended_si_o2, na2_o=blended_na2_o)
        blended_powder.composition = composition

    def _compute_mean_with_default(self, normalized_ratios, base_powders_as_dict, *keys):
        all_filled = True
        all_values = []

        for current_powder in base_powders_as_dict:
            value = self._extract_value_for_key(current_powder, keys)
            all_values.append(value)

            if value is None:
                all_filled = False

        if not all_filled:
            return None

        ratios_with_property_values = zip(normalized_ratios, all_values)
        return sum(list(map(lambda x: x[0] * string_to_number(x[1]), ratios_with_property_values)))

    def _extract_value_for_key(self, current_powder_as_dict, keys):
        base = current_powder_as_dict
        for key in keys:
            value = base.get(key, None)
            try:
                base = value.__dict__
            except AttributeError:
                return value

        raise ValueNotSupportedException('No such property!')
