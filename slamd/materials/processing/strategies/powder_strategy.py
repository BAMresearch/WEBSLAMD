from functools import reduce

from slamd.common.slamd_utils import string_to_number, numeric, not_numeric
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.base_material_strategy import MaterialStrategy


class PowderStrategy(MaterialStrategy):

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

    def create_blended_material(self, idx, blended_material_name, normalized_ratios, base_powders_as_dict):
        costs = self.compute_blended_costs(normalized_ratios, base_powders_as_dict)
        composition = self._compute_blended_composition(normalized_ratios, base_powders_as_dict)
        structure = self._compute_blended_structure(normalized_ratios, base_powders_as_dict)
        additional_properties = self._compute_additional_properties(normalized_ratios, base_powders_as_dict)

        return Powder(type=base_powders_as_dict[0]['type'],
                      name=f'{blended_material_name}-{idx}',
                      costs=costs,
                      composition=composition,
                      structure=structure,
                      additional_properties=additional_properties,
                      is_blended=True,
                      blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios))

    def _compute_blended_composition(self, normalized_ratios, base_powders_as_dict):
        blended_fe2_o3 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'fe3_o2')
        blended_si_o2 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'si_o2')
        blended_al2_o3 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'al2_o3')
        blended_na2_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'na2_o')

        blended_ca_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'ca_o')
        blended_mg_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'mg_o')
        blended_k2_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'k2_o')
        blended_s_o3 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 's_o3')

        blended_ti_o2 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'ti_o2')
        blended_p2_o5 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'p2_o5')
        blended_sr_o = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'sr_o')
        blended_mn2_o3 = self.compute_mean(normalized_ratios, base_powders_as_dict, 'composition', 'mn2_o3')

        composition = Composition(fe3_o2=blended_fe2_o3, si_o2=blended_si_o2, al2_o3=blended_al2_o3,
                                  na2_o=blended_na2_o, ca_o=blended_ca_o, mg_o=blended_mg_o,
                                  k2_o=blended_k2_o, s_o3=blended_s_o3, ti_o2=blended_ti_o2,
                                  p2_o5=blended_p2_o5, sr_o=blended_sr_o, mn2_o3=blended_mn2_o3)

        return composition

    def _compute_blended_structure(self, normalized_ratios, base_powders_as_dict):
        blended_fine = self.compute_mean(normalized_ratios, base_powders_as_dict, 'structure', 'fine')
        blended_gravity = self.compute_mean(normalized_ratios, base_powders_as_dict, 'structure', 'gravity')

        return Structure(fine=blended_fine, gravity=blended_gravity)

    def _compute_additional_properties(self, normalized_ratios, base_materials_as_dict):
        additional_properties_for_all_base_materials = []
        for base_powder in base_materials_as_dict:
            additional_properties_for_all_base_materials.append(base_powder['additional_properties'])

        properties_with_key_defined_in_all_base_materials = reduce(lambda x, y: self._keep_matching(x, y),
                                                                   additional_properties_for_all_base_materials)
        key_defined_in_all_base_materials = list(
            map(lambda prop: prop.name, properties_with_key_defined_in_all_base_materials))

        matching_properties_for_all_base_materials = []
        for base_material_dict in base_materials_as_dict:
            matching_properties_for_base_material = list(
                filter(lambda prop: prop.name in key_defined_in_all_base_materials,
                       base_material_dict['additional_properties']))

            matching_properties_for_all_base_materials.append(matching_properties_for_base_material)

        blended_additional_properties = []
        for i in range(len(matching_properties_for_all_base_materials[0])):
            ratios_with_property_values = zip(normalized_ratios, matching_properties_for_all_base_materials)

            # Create list of property names together with their weigthed values and an information about the
            # current ratio, e.g [('Prop1', 1.0, 0.5), ('Prop1', 2.0, 0.5)]
            mapped_properties = list(map(lambda x: self.method_name(x[0], x[1][i]), ratios_with_property_values))
            if numeric(mapped_properties[0][1]):
                mean = sum(list(map(lambda x: x[1], mapped_properties)))
                blended_additional_properties.append(
                    AdditionalProperty(name=mapped_properties[0][0], value=str(round(mean, 2))))
            else:
                for item in mapped_properties:
                    blended_property_names = [x.name for x in blended_additional_properties]
                    if item[1] in blended_property_names:
                        index_of_matching_name = blended_property_names.index(item[1])
                        updated_value = float(blended_additional_properties[index_of_matching_name].value) + item[2]
                        blended_additional_properties[index_of_matching_name].value = str(round(updated_value, 2))
                    else:
                        blended_additional_properties.append(
                            AdditionalProperty(name=item[1], value=str(round(item[2], 2))))
        return blended_additional_properties

    def method_name(self, ratio, property):
        return property.name, self._map_according_to_value(ratio, property.value), ratio

    def _map_according_to_value(self, ratio, value):
        if numeric(value):
            return ratio * string_to_number(value)
        return value

    # we throw away all properties with keys (names) either not contained in additional_properties of all base materials
    # or if the key is contained in additional_properties of all base materials but the types of the values are not
    # matching as otherwise we cannot clearly separate continuous from categorical variables
    def _keep_matching(self, first_property_list, second_property_list):
        return [x for x in first_property_list if
                self._is_contained_and_has_same_type_in_all_materials(x, second_property_list)]

    def _is_contained_and_has_same_type_in_all_materials(self, prop, property_list):
        matching_name = False
        matching_type = False
        names_of_properties = list(map(lambda p: p.name, property_list))
        if prop.name in names_of_properties:
            matching_name = True
        if matching_name:
            for additional_property in property_list:
                if additional_property.name == prop.name:
                    if (numeric(additional_property.value) and not_numeric(prop.value)) or (
                            not_numeric(additional_property.value) and numeric(prop.value)):
                        matching_type = False
                    else:
                        matching_type = True
        return matching_name and matching_type
