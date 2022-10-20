from slamd.common.error_handling import MaterialNotFoundException
from slamd.common.slamd_utils import empty, not_empty
from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse


class BaseMaterialService(MaterialsService):

    @classmethod
    def create_materials_response(cls, materials):
        return MaterialsResponse(materials, 'base materials / processes')

    @classmethod
    def create_material_form(cls, material_type):
        form = MaterialFactory.create_material_form(material_type=material_type)
        if material_type == 'process':
            form.co2_footprint.label.text = 'CO₂ footprint (kg)'
            form.costs.label.text = 'Costs (€)'
        else:
            form.co2_footprint.label.text = 'CO₂ footprint (kg/ton)'
            form.costs.label.text = 'Costs (€/kg)'

        form.submit.render_kw = {'disabled': 'disabled'}
        return form

    @classmethod
    def create_additional_property_form(cls, additional_property_entries):
        form = MaterialsForm()
        if not_empty(additional_property_entries):
            for entry in additional_property_entries:
                additional_property_entry = form.additional_properties.append_entry()
                additional_property_entry.property_name.data = entry['property_name']
                additional_property_entry.property_value.data = entry['property_value']

        form.additional_properties.append_entry()
        return form

    @classmethod
    def populate_form(cls, material_type, uuid):
        material = MaterialsPersistence.query_by_type_and_uuid(material_type, uuid)
        if empty(material):
            raise MaterialNotFoundException('Material with given UUID not found')
        strategy = MaterialFactory.create_strategy(material.type.lower())
        form_data = strategy.convert_to_multidict(material)
        form = MaterialFactory.create_material_form(submitted_material=form_data)
        return form

    @classmethod
    def edit_material(cls, material_type, uuid, submitted_material):
        """
        Edit a base material with type material_type and given UUID.
        The old version of the material will be deleted before creating the new one
        to keep the database consistent. The UUID is reused, even if the material_type changes.
        """
        form = MaterialFactory.create_material_form(submitted_material=submitted_material)

        if form.validate():
            cls.delete_material(material_type, uuid)
            strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
            model = strategy.edit_model(uuid, submitted_material)
            strategy.save_model(model)
            return True, None
        return False, form

    @classmethod
    def save_material(cls, submitted_material):
        form = MaterialFactory.create_material_form(submitted_material=submitted_material)

        if form.validate():
            strategy = MaterialFactory.create_strategy(submitted_material['material_type'].lower())
            model = strategy.create_model(submitted_material)
            strategy.save_model(model)
            return True, None
        return False, form

    @classmethod
    def delete_material(cls, material_type, uuid):
        MaterialsPersistence.delete_by_type_and_uuid(material_type, uuid)
