from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.materials_persistence import MaterialsPersistence


class BlendedMaterialsService:

    def list_material_selection_by_type(self, material_type):
        materials_by_type = MaterialsPersistence.query_by_type(material_type)

        material_selection = []
        for material in materials_by_type:
            material_selection.append((material.uuid, material.name))

        form = BaseMaterialSelectionForm()
        form.base_material_selection.choices = material_selection
        return form
