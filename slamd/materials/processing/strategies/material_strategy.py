from abc import ABC, abstractmethod
from dataclasses import asdict
from uuid import UUID

from werkzeug.datastructures import MultiDict

from slamd.common.error_handling import ValueNotSupportedException, SlamdUnprocessableEntityException
from slamd.common.slamd_utils import empty, not_empty, numeric, string_to_number_or_string, write_dict_into_object
from slamd.common.slamd_utils import join_all, float_if_not_empty, str_if_not_none
from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs, Material
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker

INVALID_START_OF_FEATURE_NAME = 'Target'


class MaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_model(cls, submitted_material):
        pass

    @classmethod
    @abstractmethod
    def gather_composition_information(cls, material):
        pass

    @classmethod
    def convert_material_to_dict(cls, material):
        out = asdict(material)
        out['uuid'] = str(material.uuid)
        if material.costs:
            out['costs'] = asdict(material.costs)
        if material.additional_properties:
            out['additional_properties'] = [asdict(prop) for prop in material.additional_properties]
        if material.created_from:
            out['created_from'] = [str(uuid) for uuid in material.created_from]

        return out

    @classmethod
    def create_material_from_dict(cls, dictionary):
        mat = Material()
        cls.fill_material_object_with_basic_info_from_dict(mat, dictionary)
        return mat

    @classmethod
    def fill_material_object_with_basic_info_from_dict(cls, mat, dictionary):
        write_dict_into_object(dictionary, mat)

        if dictionary['uuid']:
            mat.uuid = UUID(dictionary['uuid'])
        else:
            raise SlamdUnprocessableEntityException(message='Error while attempting to construct Material from dict: '
                                                            'No UUID')

        if dictionary['costs']:
            new_costs = Costs()
            write_dict_into_object(dictionary['costs'], new_costs)
            mat.costs = new_costs

        if dictionary['created_from']:
            mat.created_from = [UUID(uuid_str) for uuid_str in dictionary['created_from']]

        if dictionary['additional_properties']:
            mat.additional_properties = [AdditionalProperty(name=p['name'], value=p['value'])
                                         for p in dictionary['additional_properties']]

    @classmethod
    def for_formulation(cls, material):
        multidict = MultiDict([
            (f'delivery_time ({material.type})', float_if_not_empty(material.costs.delivery_time)),
            (f'costs ({material.type})', float_if_not_empty(material.costs.costs)),
            (f'co2_footprint ({material.type})', float_if_not_empty(material.costs.co2_footprint)),
        ])
        cls._convert_additional_properties_for_formulation(multidict, material)
        return multidict

    @classmethod
    def create_dto(cls, material):
        dto = MaterialDto(
            uuid=str(material.uuid),
            name=material.name,
            material_type=material.type,
            all_properties=join_all(cls.gather_composition_information(material))
        )

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
            ('delivery_time', str_if_not_none(material.costs.delivery_time)),
            ('costs', str_if_not_none(material.costs.costs)),
            ('co2_footprint', str_if_not_none(material.costs.co2_footprint)),
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

        if len(submitted_names) != len(set(submitted_names)):
            raise ValueNotSupportedException('Names for additional properties must be unique')

        for name, value in zip(submitted_names, submitted_values):
            if name.startswith(INVALID_START_OF_FEATURE_NAME) or value.startswith(INVALID_START_OF_FEATURE_NAME):
                raise ValueNotSupportedException('You cannot use Target as a feature!')
            if not_empty(name):
                additional_property = AdditionalProperty(name, string_to_number_or_string(value))
                additional_properties.append(additional_property)

        return additional_properties

    @classmethod
    def extract_cost_properties(cls, submitted_material):
        return Costs(
            co2_footprint=float_if_not_empty(submitted_material['co2_footprint']),
            costs=float_if_not_empty(submitted_material['costs']),
            delivery_time=float_if_not_empty(submitted_material['delivery_time'])
        )

    @classmethod
    def include(cls, displayed_name, property_value):
        if empty(property_value):
            return ''
        return f'{displayed_name}: {property_value}, '

    @classmethod
    def save_model(cls, model):
        MaterialsPersistence.save(model.type.lower(), model)

    @classmethod
    def _append_cost_properties(cls, dto, costs):
        if costs is None:
            return
        dto.all_properties += cls.include('Costs (€/ton for materials, € for processes)', costs.costs)
        dto.all_properties += cls.include('CO₂ footprint (kg/ton for materials, kg for processes)', costs.co2_footprint)
        dto.all_properties += cls.include('Delivery time (days)', costs.delivery_time)

    @classmethod
    def _append_additional_properties(cls, dto, additional_properties):
        if additional_properties is None or len(additional_properties) == 0:
            return

        additional_property_to_be_displayed = ''
        for prop in additional_properties:
            additional_property_to_be_displayed += f'{prop.name}: {prop.value}, '
        dto.all_properties += additional_property_to_be_displayed

    @classmethod
    def _convert_additional_properties_to_multidict(cls, multidict, additional_properties):
        for (index, prop) in enumerate(additional_properties):
            multidict.add(f'additional_properties-{index}-property_name', prop.name)
            multidict.add(f'additional_properties-{index}-property_value', prop.value)

    @classmethod
    def _convert_additional_properties_for_formulation(cls, multidict, material):
        for prop in material.additional_properties:
            value = prop.value
            if numeric(value):
                value = float(value)
            multidict.add(prop.name, value)

    @classmethod
    def _extract_additional_property_by_label(cls, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional_properties' in k and label in k]

    @classmethod
    def create_blended_material(cls, name, normalized_ratios, base_materials_as_dict):
        pass

    @classmethod
    def created_from(cls, base_materials_as_dict):
        return [material['uuid'] for material in base_materials_as_dict]

    @classmethod
    def check_completeness_of_base_material_properties(cls, base_materials_as_dict):
        pass

    @classmethod
    def compute_blended_costs(cls, normalized_ratios, base_materials_as_dict):
        return BlendingPropertiesCalculator.compute_blended_costs(normalized_ratios, base_materials_as_dict)

    @classmethod
    def compute_additional_properties(cls, normalized_ratios, base_materials_as_dict):
        return BlendingPropertiesCalculator.compute_additional_properties(normalized_ratios, base_materials_as_dict)

    @classmethod
    def check_completeness_of_costs(cls, base_materials_as_dict):
        co2_footprint_complete = PropertyCompletenessChecker.is_complete(
            base_materials_as_dict, 'costs', 'co2_footprint')
        costs_complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'costs', 'costs')
        delivery_time_complete = PropertyCompletenessChecker.is_complete(
            base_materials_as_dict, 'costs', 'delivery_time')

        return co2_footprint_complete and costs_complete and delivery_time_complete

    @classmethod
    def check_completeness_of_additional_properties(cls, base_materials_as_dict):
        return PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)
