from abc import ABC, abstractmethod

from slamd.common.slamd_utils import empty
from slamd.common.slamd_utils import join_all
from slamd.materials.base_material_dto import BaseMaterialDto


class BaseMaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material, additional_properties):
        pass

    def _include(self, displayed_name, property):
        if empty(property):
            return ''
        return f'{displayed_name}: {property}, '

    def create_dto(self, material):
        dto = BaseMaterialDto()
        dto.name = material.name
        dto.type = material.type

        dto.all_properties = join_all(
            self._gather_composition_information(material))

        self._append_additional_properties(dto, material.additional_properties)
        # Remove trailing comma and whitespace
        dto.all_properties = dto.all_properties.strip()[:-1]
        return dto

    def _append_additional_properties(self, dto, additional_properties):
        if len(additional_properties) == 0:
            return

        additional_property_to_be_displayed = ''
        for property in additional_properties:
            additional_property_to_be_displayed += f'{property.name}: {property.value}, '
        dto.all_properties += additional_property_to_be_displayed
