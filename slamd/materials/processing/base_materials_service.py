from slamd.common.slamd_utils import not_empty
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse
from slamd.materials.processing.models.additional_property import AdditionalProperty


class BaseMaterialService(MaterialsService):

    def create_materials_response(self, materials):
        return MaterialsResponse(materials, 'base')

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        form = MaterialFactory.create_material_form(type=type)
        return template_file, form

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
        return self.list_materials(blended=False)

    def _extract_additional_property_by_label(self, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional-properties' in k and label in k]

    def _create_base_material_by_type(self, submitted_material, additional_properties):
        strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
        strategy.create_model(submitted_material, additional_properties)
