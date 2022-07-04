from abc import ABC, abstractmethod

from slamd.common.slamd_utils import empty
from slamd.common.slamd_utils import join_all
from slamd.materials.base_material_dto import BaseMaterialDto


class BaseMaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material, additional_properties):
        pass

    @abstractmethod
    def create_dto(self, material):
        pass

    def _include(self, displayed_name, property):
        if empty(property):
            return ''
        return f'{displayed_name}: {property}, '

    def create_dto(self, material):
        dto = BaseMaterialDto()
        dto.name = material.name
        dto.type = material.type

        all_properties = join_all(
            self._gather_composition_information(material))

        additional_properties = material.additional_properties
        if len(additional_properties) == 0:
            return self._set_all_properties(dto, all_properties)

        return self._add_additional_properties(all_properties, additional_properties, dto)

    def _add_additional_properties(self, all_properties, additional_properties, dto):
        additional_property_to_be_displayed = ''
        for property in additional_properties:
            additional_property_to_be_displayed += f'{property.name}: {property.value}, '
        all_properties += additional_property_to_be_displayed
        return self._set_all_properties(dto, all_properties)

    def _set_all_properties(self, dto, all_properties):
        displayed_properties = all_properties.strip()[:-1]
        dto.all_properties = displayed_properties
        return dto
