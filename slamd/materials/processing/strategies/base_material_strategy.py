from abc import ABC, abstractmethod
from werkzeug.datastructures import MultiDict

from slamd.common.slamd_utils import empty
from slamd.common.slamd_utils import join_all
from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs


class BaseMaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material, additional_properties):
        pass

    @abstractmethod
    def gather_composition_information(self, material):
        pass

    def create_dto(self, material):
        dto = MaterialDto()
        dto.uuid = str(material.uuid)
        dto.name = material.name
        dto.type = material.type

        dto.all_properties = join_all(
            self.gather_composition_information(material))

        self._append_cost_properties(dto, material.costs)
        self._append_additional_properties(dto, material.additional_properties)
        # Remove trailing comma and whitespace
        dto.all_properties = dto.all_properties.strip()[:-1]
        return dto

    def convert_to_multidict(self, material):
        multidict = MultiDict([
            ('uuid', material.uuid),
            ('material_name', material.name),
            ('material_type', material.type),
            ('delivery_time', material.costs.delivery_time),
            ('costs', material.costs.costs),
            ('co2_footprint', material.costs.co2_footprint),
            ('is_blended', material.is_blended)
        ])
        self._convert_additional_properties_to_multidict(multidict, material.additional_properties)
        return multidict

    def edit_model(self, uuid, submitted_material, additional_properties):
        model = self.create_model(submitted_material, additional_properties)
        model.uuid = uuid
        return model

    def extract_cost_properties(self, submitted_material):
        return Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

    def include(self, displayed_name, property):
        if empty(property):
            return ''
        return f'{displayed_name}: {property}, '

    def save_model(self, material):
        material_type = material.type.lower()
        MaterialsPersistence.save(material_type, material)

    def _append_cost_properties(self, dto, costs):
        if costs is None:
            return
        dto.all_properties += self.include('Costs (€/kg)', costs.costs)
        dto.all_properties += self.include('CO₂ footprint (kg)',
                                           costs.co2_footprint)
        dto.all_properties += self.include(
            'Delivery time (days)', costs.delivery_time)

    def _append_additional_properties(self, dto, additional_properties):
        if additional_properties is None or len(additional_properties) == 0:
            return

        additional_property_to_be_displayed = ''
        for property in additional_properties:
            additional_property_to_be_displayed += f'{property.name}: {property.value}, '
        dto.all_properties += additional_property_to_be_displayed

    def _convert_additional_properties_to_multidict(self, multidict, additional_properties):
        for (index, property) in enumerate(additional_properties):
            multidict.add(f'additional_properties-{index}-property_name', property.name)
            multidict.add(f'additional_properties-{index}-property_value', property.value)
