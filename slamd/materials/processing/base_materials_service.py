from werkzeug.exceptions import NotFound

from slamd.common.slamd_utils import not_empty
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty


class BaseMaterialService:

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        form = MaterialFactory.create_material_form(type=type)
        return template_file, form

    def list_all(self):
        all_material_types = MaterialType.get_all_types()

        all_material_dtos = []
        for material_type in all_material_types:
            materials = MaterialsPersistence.query_by_type(material_type)
            strategy = MaterialFactory.create_strategy(material_type)
            for material in materials:
                dto = strategy.create_dto(material)
                all_material_dtos.append(dto)

        sorted_by_name = sorted(all_material_dtos, key=lambda material: material.name)
        sorted_by_type = sorted(sorted_by_name, key=lambda material: material.type)
        return sorted_by_type

    def find_material(self, uuid):
        all_material_types = MaterialType.get_all_types()
        for material_type in all_material_types:
            match = MaterialsPersistence.query_by_type_and_uuid(material_type, uuid)
            if match:
                return match
        # Nothing found
        raise NotFound

    def save_material(self, submitted_material):
        form = MaterialFactory.create_material_form(submitted_material=submitted_material)

        additional_properties = []
        submitted_names = self._extract_additional_property_by_label(submitted_material, 'name')
        submitted_values = self._extract_additional_property_by_label(submitted_material, 'value')

        for name, value in zip(submitted_names, submitted_values):
            if not_empty(name):
                additional_property = AdditionalProperty(name, value)
                additional_properties.append(additional_property)

        if form.validate():
            self._create_base_material_by_type(submitted_material, additional_properties)
            return True, None
        return False, form

    def delete_material(self, type, uuid):
        MaterialsPersistence.delete_by_type_and_uuid(type, uuid)
        return self.list_all()

    def _extract_additional_property_by_label(self, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional-properties' in k and label in k]

    def _create_base_material_by_type(self, submitted_material, additional_properties):
        strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
        strategy.create_model(submitted_material, additional_properties)
