from flask import session

from slamd.common.slamd_utils import empty
from slamd.materials.base_material_dto import BaseMaterialDto
from slamd.materials.model.base_material import Costs
from slamd.materials.model.powder import Powder, Composition, Structure


class PowderStrategy:

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

        before = session.get('powder_list', None)

        if before is None:
            session['powder_list'] = [powder]
        else:
            session['powder_list'].append(powder)

    def create_dto(self, powder):
        dto = BaseMaterialDto()
        dto.name = powder.name
        dto.type = powder.type

        further_information = self._join_all([self._include('FeO', powder.composition.feo), self._include('SiO', powder.composition.sio)])
        additional_properties = powder.additional_properties
        if len(additional_properties) == 0:
            displayed_information = further_information[:-1]
            dto.further_information = displayed_information
            return dto

        for i, property in enumerate(additional_properties):
            further_information.join(f' {property.name}: {property.value},')

        displayed_information = further_information[:-1]
        dto.further_information = displayed_information
        return dto

    def _include(self, displayed_name, property):
        if empty(property):
            return ''
        return f' {displayed_name}: {property},'

    def _join_all(self, input_list):
        return ''.join(input for input in input_list)
