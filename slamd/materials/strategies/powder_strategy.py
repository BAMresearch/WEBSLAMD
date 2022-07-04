from slamd.common.slamd_utils import join_all, molecular_formula_of
from slamd.materials.base_material_dto import BaseMaterialDto
from slamd.materials.materials_persistence import MaterialsPersistence
from slamd.materials.model.base_material import Costs
from slamd.materials.model.powder import Powder, Composition, Structure
from slamd.materials.strategies.base_material_strategy import BaseMaterialStrategy


class PowderStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        composition = Composition()
        composition.fe3_o2 = submitted_material['fe3_o2']
        composition.si_o2 = submitted_material['si_o2']
        composition.al2_o3 = submitted_material['al2_o3']
        composition.ca_o = submitted_material['ca_o']
        composition.mg_o = submitted_material['mg_o']
        composition.na2_o = submitted_material['na2_o']
        composition.k2_o = submitted_material['k2_o']
        composition.s_o3 = submitted_material['s_o3']
        composition.ti_o2 = submitted_material['ti_o2']
        composition.p2_o5 = submitted_material['p2_o5']
        composition.sr_o = submitted_material['sr_o']
        composition.mn2_o3 = submitted_material['mn2_o3']

        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        structure = Structure()
        structure.gravity = submitted_material['gravity']
        structure.fine = submitted_material['fine']

        powder = Powder()

        powder.name = submitted_material['material_name']
        powder.type = submitted_material['material_type']
        powder.costs = costs
        powder.composition = composition
        powder.structure = structure
        powder.additional_properties = additional_properties

        MaterialsPersistence.save('powder', powder)

    def create_dto(self, powder):
        dto = BaseMaterialDto()
        dto.name = powder.name
        dto.type = powder.type

        all_properties = join_all(self._gather_composition_information(powder))

        additional_properties = powder.additional_properties
        if len(additional_properties) == 0:
            return self._set_all_properties(dto, all_properties)

        return self._add_additional_properties(all_properties, additional_properties, dto)

    def _add_additional_properties(self, all_properties, additional_properties, dto):
        additioal_property_to_be_displayed = ''
        for property in additional_properties:
            additioal_property_to_be_displayed += f'{property.name}: {property.value}, '
        all_properties += additioal_property_to_be_displayed
        return self._set_all_properties(dto, all_properties)

    def _set_all_properties(self, dto, all_properties):
        displayed_properties = all_properties.strip()[:-1]
        dto.all_properties = displayed_properties
        return dto

    def _gather_composition_information(self, powder):
        return [self._include(molecular_formula_of('Fe2O3'),
                              powder.composition.fe3_o2),
                self._include(molecular_formula_of('SiO2'),
                              powder.composition.si_o2),
                self._include(molecular_formula_of('Al2O3'),
                              powder.composition.al2_o3),
                self._include(molecular_formula_of('CaO'),
                              powder.composition.ca_o),
                self._include(molecular_formula_of('MgO'),
                              powder.composition.mg_o),
                self._include(molecular_formula_of('Na2O'),
                              powder.composition.na2_o),
                self._include(molecular_formula_of('K2O'),
                              powder.composition.k2_o),
                self._include(molecular_formula_of('SO3'),
                              powder.composition.s_o3),
                self._include(molecular_formula_of('TiO2'),
                              powder.composition.ti_o2),
                self._include(molecular_formula_of('P2O5'),
                              powder.composition.p2_o5),
                self._include(molecular_formula_of('SrO'),
                              powder.composition.sr_o),
                self._include(molecular_formula_of('Mn2O3'),
                              powder.composition.mn2_o3),
                self._include('Fine modules', powder.structure.fine),
                self._include('Specific gravity', powder.structure.gravity)]
