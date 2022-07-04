from slamd.common.slamd_utils import join_all, molecular_formula_of
from slamd.materials.base_material_dto import BaseMaterialDto
from slamd.materials.materials_persistence import MaterialsPersistence
from slamd.materials.model.base_material import Costs
from slamd.materials.model.powder import Powder, Composition, Structure
from slamd.materials.strategies.base_material_strategy import BaseMaterialStrategy


class PowderStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        composition = Composition()
        composition.feo = submitted_material['feo']
        composition.sio = submitted_material['sio']

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
        return [self._include(molecular_formula_of('Fe2O3'), powder.composition.feo),
                self._include(molecular_formula_of('SiO2'), powder.composition.sio),
                self._include('Fine modules', powder.structure.fine),
                self._include('Specific gravity', powder.structure.gravity)]
