from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import not_numeric
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.materials.processing.materials_persistence import MaterialsPersistence


class FormulationsService:

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsPersistence.find_all_materials()

        flattened_materials = []
        for materials_for_type in all_materials:
            for material in materials_for_type:
                flattened_materials.append(material)

        materials_for_selection = cls._to_selection(flattened_materials)

        all_processes = MaterialsPersistence.find_all_processes()
        processes_for_selection = cls._to_selection(all_processes)

        form = MaterialsAndProcessesSelectionForm()
        form.material_selection.choices = materials_for_selection
        form.process_selection.choices = processes_for_selection

        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (material.uuid, f'{material.type.capitalize()}: {material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, count):
        if not_numeric(count):
            raise ValueNotSupportedException('Cannot process selection!')

        count = int(count)

        if count == 0:
            raise ValueNotSupportedException('No item selected!')

        min_max_form = FormulationsMinMaxForm()
        for i in range(count):
            min_max_form.all_formulations_min_max_entries.append_entry()
        return min_max_form
