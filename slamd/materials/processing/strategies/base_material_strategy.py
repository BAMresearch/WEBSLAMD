from abc import ABC, abstractmethod

from werkzeug.datastructures import MultiDict

from slamd.common.slamd_utils import empty, not_empty
from slamd.common.slamd_utils import join_all
from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


class MaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material):
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

    def edit_model(self, uuid, submitted_material):
        model = self.create_model(submitted_material)
        model.uuid = uuid
        return model

    def extract_additional_properties(self, submitted_material):
        additional_properties = []
        submitted_names = self._extract_additional_property_by_label(submitted_material, 'name')
        submitted_values = self._extract_additional_property_by_label(submitted_material, 'value')

        for name, value in zip(submitted_names, submitted_values):
            if not_empty(name):
                additional_property = AdditionalProperty(name, value)
                additional_properties.append(additional_property)
        return additional_properties

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

    def save_model(self, model):
        MaterialsPersistence.save(model.type.lower(), model)

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

    def _extract_additional_property_by_label(self, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional_properties' in k and label in k]

    def create_blended_material(self, idx, blended_material_name, normalized_ratios, base_powders):
        pass

    def check_completeness_of_base_material_properties(self, base_materials_as_dict):
        pass

    def compute_blended_costs(self, normalized_ratios, base_materials_as_dict):
        return BlendingPropertiesCalculator.compute_blended_costs(normalized_ratios, base_materials_as_dict)

    def compute_additional_properties(self, normalized_ratios, base_materials_as_dict):
        return BlendingPropertiesCalculator.compute_additional_properties(normalized_ratios, base_materials_as_dict)

    def check_completeness_of_costs(self, base_materials_as_dict):
        co2_footprint_complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'costs',
                                                                         'co2_footprint')
        costs_complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'costs', 'costs')
        delivery_time_complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'costs',
                                                                         'delivery_time')

        return co2_footprint_complete and costs_complete and delivery_time_complete

    def check_completeness_of_additional_properties(self, base_materials_as_dict):
        return PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)
