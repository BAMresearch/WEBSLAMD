from slamd.common.error_handling import MaterialNotFoundException
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence


class BlendedMaterialsService:

    def list_material_selection_by_type(self, material_type):
        if material_type not in MaterialType.get_all_types():
            raise MaterialNotFoundException('The requested type is not supported!')

        materials_by_type = MaterialsPersistence.query_by_type(material_type)

        material_selection = []
        for material in materials_by_type:
            material_selection.append((material.uuid, material.name))

        form = BaseMaterialSelectionForm()
        form.base_material_selection.choices = material_selection
        return form

    def create_min_max_form(self, count):
        min_max_form = MinMaxForm()
        for i in range(int(count)):
            min_max_form.all_min_max_entries.append_entry()
        return min_max_form
