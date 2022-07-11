from abc import ABC, abstractmethod

from slamd.common.slamd_utils import empty
from slamd.common.slamd_utils import join_all
from slamd.materials.processing.material_dto import MaterialDto


class BaseMaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material, additional_properties):
        pass

    def _include(self, displayed_name, property):
        if empty(property):
            return ''
        return f'{displayed_name}: {property}, '

    def create_dto(self, material):
        dto = MaterialDto()
        dto.uuid = str(material.uuid)
        dto.name = material.name
        dto.type = material.type

        dto.all_properties = join_all(
            self._gather_composition_information(material))

        self._append_cost_properties(dto, material.costs)
        self._append_additional_properties(dto, material.additional_properties)
        # Remove trailing comma and whitespace
        dto.all_properties = dto.all_properties.strip()[:-1]
        return dto

    def _append_cost_properties(self, dto, costs):
        if costs is None:
            return
        dto.all_properties += self._include('Costs (€/kg)', costs.costs)
        dto.all_properties += self._include('CO₂ footprint (kg)',
                                            costs.co2_footprint)
        dto.all_properties += self._include(
            'Delivery time (days)', costs.delivery_time)

    def _append_additional_properties(self, dto, additional_properties):
        if additional_properties is None or len(additional_properties) == 0:
            return

        additional_property_to_be_displayed = ''
        for property in additional_properties:
            additional_property_to_be_displayed += f'{property.name}: {property.value}, '
        dto.all_properties += additional_property_to_be_displayed
