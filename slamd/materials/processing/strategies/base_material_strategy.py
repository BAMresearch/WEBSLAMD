from abc import ABC, abstractmethod
from functools import reduce

from werkzeug.datastructures import MultiDict

from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import empty, string_to_number, not_empty, numeric, not_numeric
from slamd.common.slamd_utils import join_all
from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs


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

    def compute_blended_costs(self, normalized_ratios, base_materials_as_dict):
        blended_co2_footprint = self.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'co2_footprint')
        blended_costs = self.compute_mean(normalized_ratios, base_materials_as_dict, 'costs', 'costs')
        blended_delivery_time = self.compute_max(base_materials_as_dict, 'costs', 'delivery_time')

        return Costs(co2_footprint=blended_co2_footprint, costs=blended_costs, delivery_time=blended_delivery_time)

    def compute_mean(self, normalized_ratios, materials_as_dict, *keys):
        all_values = self._collect_all_base_material_values_for_property(materials_as_dict, keys)

        empty_values = [value for value in all_values if empty(value)]

        if len(empty_values) > 0:
            return None

        ratios_with_property_values = zip(normalized_ratios, all_values)
        mean = sum(list(map(lambda x: x[0] * string_to_number(x[1]), ratios_with_property_values)))
        return str(round(mean, 2))

    def compute_max(self, material_as_dict, *keys):
        all_values = self._collect_all_base_material_values_for_property(material_as_dict, keys)
        non_empty_values = [float(value) for value in all_values if not_empty(value)]
        if len(non_empty_values) == 0:
            return None
        maximum = max(non_empty_values)
        return str(round(maximum, 2))

    def _collect_all_base_material_values_for_property(self, material_as_dict, keys):
        all_values = []

        for current_powder in material_as_dict:
            value = self._extract_value_for_key(current_powder, keys)
            all_values.append(value)

        return all_values

    def _extract_value_for_key(self, material_as_dict, keys):
        base = material_as_dict
        for key in keys:
            value = base.get(key, None)
            try:
                base = value.__dict__
            except AttributeError:
                return value

        raise ValueNotSupportedException('No such property!')

    def compute_additional_properties(self, normalized_ratios, base_materials_as_dict):
        additional_properties_for_all_base_materials = []
        for base_powder in base_materials_as_dict:
            additional_properties_for_all_base_materials.append(base_powder['additional_properties'])

        properties_with_key_defined_in_all_base_materials = reduce(lambda x, y: self._keep_matching(x, y),
                                                                   additional_properties_for_all_base_materials)
        key_defined_in_all_base_materials = list(
            map(lambda prop: prop.name, properties_with_key_defined_in_all_base_materials))

        matching_properties_for_all_base_materials = []
        for base_material_dict in base_materials_as_dict:
            matching_properties_for_base_material = list(
                filter(lambda prop: prop.name in key_defined_in_all_base_materials,
                       base_material_dict['additional_properties']))

            matching_properties_for_all_base_materials.append(matching_properties_for_base_material)

        blended_additional_properties = []
        for i in range(len(matching_properties_for_all_base_materials[0])):
            ratios_with_property_values = zip(normalized_ratios, matching_properties_for_all_base_materials)

            # Create list of property names together with their weigthed values and an information about the
            # current ratio, e.g [('Prop1', 1.0, 0.5), ('Prop1', 2.0, 0.5)]
            mapped_properties = list(map(lambda x: self.method_name(x[0], x[1][i]), ratios_with_property_values))
            if numeric(mapped_properties[0][1]):
                mean = sum(list(map(lambda x: x[1], mapped_properties)))
                blended_additional_properties.append(
                    AdditionalProperty(name=mapped_properties[0][0], value=str(round(mean, 2))))
            else:
                for item in mapped_properties:
                    blended_property_names = [x.name for x in blended_additional_properties]
                    if item[1] in blended_property_names:
                        index_of_matching_name = blended_property_names.index(item[1])
                        updated_value = float(blended_additional_properties[index_of_matching_name].value) + item[2]
                        blended_additional_properties[index_of_matching_name].value = str(round(updated_value, 2))
                    else:
                        blended_additional_properties.append(
                            AdditionalProperty(name=item[1], value=str(round(item[2], 2))))
        return blended_additional_properties

    def method_name(self, ratio, property):
        return property.name, self._map_according_to_value(ratio, property.value), ratio

    def _map_according_to_value(self, ratio, value):
        if numeric(value):
            return ratio * string_to_number(value)
        return value

    # we throw away all properties with keys (names) either not contained in additional_properties of all base materials
    # or if the key is contained in additional_properties of all base materials but the types of the values are not
    # matching as otherwise we cannot clearly separate continuous from categorical variables
    def _keep_matching(self, first_property_list, second_property_list):
        return [x for x in first_property_list if
                self._is_contained_and_has_same_type_in_all_materials(x, second_property_list)]

    def _is_contained_and_has_same_type_in_all_materials(self, prop, property_list):
        matching_name = False
        matching_type = False
        names_of_properties = list(map(lambda p: p.name, property_list))
        if prop.name in names_of_properties:
            matching_name = True
        if matching_name:
            for additional_property in property_list:
                if additional_property.name == prop.name:
                    if (numeric(additional_property.value) and not_numeric(prop.value)) or (
                            not_numeric(additional_property.value) and numeric(prop.value)):
                        matching_type = False
                    else:
                        matching_type = True
        return matching_name and matching_type
