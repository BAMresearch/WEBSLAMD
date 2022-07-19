from abc import ABC, abstractmethod
from werkzeug.datastructures import MultiDict

from slamd.common.slamd_utils import not_empty, empty, join_all
from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs


class BaseMaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_model(cls, submitted_material):
        pass

    @classmethod
    @abstractmethod
    def gather_composition_information(cls, material):
        pass

    @classmethod
    def create_dto(cls, material):
        dto = MaterialDto()
        dto.uuid = str(material.uuid)
        dto.name = material.name
        dto.type = material.type

        dto.all_properties = join_all(cls.gather_composition_information(material))

        cls._append_cost_properties(dto, material.costs)
        cls._append_additional_properties(dto, material.additional_properties)
        # Remove trailing comma and whitespace
        dto.all_properties = dto.all_properties.strip()[:-1]
        return dto

    @classmethod
    def convert_to_multidict(cls, material):
        multidict = MultiDict([
            ('uuid', material.uuid),
            ('material_name', material.name),
            ('material_type', material.type),
            ('delivery_time', material.costs.delivery_time),
            ('costs', material.costs.costs),
            ('co2_footprint', material.costs.co2_footprint),
            ('is_blended', material.is_blended)
        ])
        cls._convert_additional_properties_to_multidict(multidict, material.additional_properties)
        return multidict

    @classmethod
    def edit_model(cls, uuid, submitted_material):
        model = cls.create_model(submitted_material)
        model.uuid = uuid
        return model

    @classmethod
    def extract_additional_properties(cls, submitted_material):
        additional_properties = []
        submitted_names = cls._extract_additional_property_by_label(submitted_material, 'name')
        submitted_values = cls._extract_additional_property_by_label(submitted_material, 'value')

        for name, value in zip(submitted_names, submitted_values):
            if not_empty(name):
                additional_property = AdditionalProperty(name, value)
                additional_properties.append(additional_property)
        return additional_properties

    @classmethod
    def extract_cost_properties(cls, submitted_material):
        return Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

    @classmethod
    def include(cls, displayed_name, property):
        if empty(property):
            return ''
        return f'{displayed_name}: {property}, '

    @classmethod
    def save_model(cls, model):
        MaterialsPersistence.save(model.type.lower(), model)

    @classmethod
    def _append_cost_properties(cls, dto, costs):
        if costs is None:
            return
        dto.all_properties += cls.include('Costs (€/kg)', costs.costs)
        dto.all_properties += cls.include('CO₂ footprint (kg)', costs.co2_footprint)
        dto.all_properties += cls.include('Delivery time (days)', costs.delivery_time)

    @classmethod
    def _append_additional_properties(cls, dto, additional_properties):
        if additional_properties is None or len(additional_properties) == 0:
            return

        additional_property_to_be_displayed = ''
        for property in additional_properties:
            additional_property_to_be_displayed += f'{property.name}: {property.value}, '
        dto.all_properties += additional_property_to_be_displayed

    @classmethod
    def _convert_additional_properties_to_multidict(cls, multidict, additional_properties):
        for (index, property) in enumerate(additional_properties):
            multidict.add(f'additional_properties-{index}-property_name', property.name)
            multidict.add(f'additional_properties-{index}-property_value', property.value)

    @classmethod
    def _extract_additional_property_by_label(cls, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional_properties' in k and label in k]
