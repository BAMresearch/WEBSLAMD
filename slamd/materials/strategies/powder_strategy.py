from flask import session

from slamd.common.slamd_utils import empty, join_all
from slamd.materials.base_material_dto import BaseMaterialDto
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

        before = session.get('powder_list', None)

        if before is None:
            session['powder_list'] = [powder]
        else:
            session['powder_list'].append(powder)

    def create_dto(self, powder):
        dto = BaseMaterialDto()
        dto.name = powder.name
        dto.type = powder.type

        further_information = join_all([self._include(u'Fe\u2082O\u2083', powder.composition.feo),
                                        self._include(u'SiO\u2082', powder.composition.sio)])
        additional_properties = powder.additional_properties
        if len(additional_properties) == 0:
            displayed_information = further_information[:-1]
            dto.further_information = displayed_information
            return dto

        for property in additional_properties:
            further_information += f' {property.name}: {property.value},'

        displayed_information = further_information[:-1]
        dto.further_information = displayed_information
        return dto
