from slamd.common.error_handling import MaterialNotFoundException
from slamd.common.slamd_utils import empty, not_empty
from slamd.materials.processing.forms.additional_properties_form import AdditionalPropertiesForm
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse


class BaseMaterialService(MaterialsService):

    def create_materials_response(self, materials):
        return MaterialsResponse(materials, 'base')

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        form = MaterialFactory.create_material_form(type=type)
        return template_file, form

    def create_additional_property_form(self, additional_property_entries):
        new_form = AdditionalPropertiesForm()
        if (not_empty(additional_property_entries)):
            for entry in additional_property_entries:
                additional_property_entry = new_form.additional_properties.append_entry()
                additional_property_entry.property_name.data = entry['property_name']
                additional_property_entry.property_value.data = entry['property_value']

        new_form.additional_properties.append_entry()
        return new_form

    def populate_form(self, material_type, uuid):
        material = MaterialsPersistence.query_by_type_and_uuid(material_type, uuid)
        if empty(material):
            raise MaterialNotFoundException('Material with given UUID not found')
        strategy = MaterialFactory.create_strategy(material.type.lower())
        form_data = strategy.convert_to_multidict(material)
        form = MaterialFactory.create_material_form(submitted_material=form_data)
        return form

    def edit_material(self, material_type, uuid, submitted_material):
        """
        Edit a base material with type material_type and given UUID.
        The old version of the material will be deleted before creating the new one
        to keep the database consistent. The UUID is reused, even if the material_type changes.
        """
        form = MaterialFactory.create_material_form(submitted_material=submitted_material)

        if form.validate():
            self.delete_material(material_type, uuid)
            strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
            model = strategy.edit_model(uuid, submitted_material)
            strategy.save_model(model)
            return True, None
        return False, form

    def save_material(self, submitted_material):
        form = MaterialFactory.create_material_form(submitted_material=submitted_material)

        if form.validate():
            strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
            model = strategy.create_model(submitted_material)
            strategy.save_model(model)
            return True, None
        return False, form

    def delete_material(self, type, uuid):
        MaterialsPersistence.delete_by_type_and_uuid(type, uuid)
        return self.list_materials(blended=False)
