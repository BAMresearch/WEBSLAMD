from functools import reduce
from itertools import product

from slamd.common.error_handling import MaterialNotFoundException, ValueNotSupportedException
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.forms.ratio_form import RatioForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse


class BlendedMaterialsService(MaterialsService):

    def create_materials_response(self, materials):
        return MaterialsResponse(materials, 'blended')

    def list_base_material_selection_by_type(self, material_type):
        if material_type not in MaterialType.get_all_types():
            raise MaterialNotFoundException('The requested type is not supported!')

        materials_by_type = MaterialsPersistence.query_by_type(material_type)
        base_materials = list(filter(lambda m: m.is_blended is False, materials_by_type))

        material_selection = []
        for material in base_materials:
            material_selection.append((material.uuid, material.name))

        form = BaseMaterialSelectionForm()
        form.base_material_selection.choices = material_selection
        return form

    def create_min_max_form(self, count):
        if not count.isnumeric():
            raise ValueNotSupportedException('Cannot process selection!')

        count = int(count)

        if count < 2:
            raise ValueNotSupportedException('At least two items must be selected!')

        min_max_form = MinMaxForm()
        for i in range(count):
            min_max_form.all_min_max_entries.append_entry()
        return min_max_form

    def create_ratio_form(self, min_max_values_with_increments):
        if not self._ratio_input_is_valid(min_max_values_with_increments):
            raise ValueNotSupportedException('Configuration of ratios is not valid!')

        all_values = []
        for i in range(len(min_max_values_with_increments) - 1):
            min = min_max_values_with_increments[i]['min']
            max = min_max_values_with_increments[i]['max']
            increment = min_max_values_with_increments[i]['increment']
            all_values.append(range(min, max + 1, increment))

        cartesian_product = product(*all_values)
        cartesian_product_list = list(cartesian_product)

        ratio_form = RatioForm()
        for entry in cartesian_product_list:
            all_ratios_for_entry = self._create_entry_value(entry)
            ratio_form_entry = ratio_form.all_ratio_entries.append_entry()
            ratio_form_entry.ratio.data = all_ratios_for_entry
        return ratio_form

    def _create_entry_value(self, entry):
        entry_list = list(entry)
        sum_of_independent_ratios = sum(entry_list)
        dependent_ratio_value = round(100 - sum_of_independent_ratios, 2)
        independent_ratio_values = "/".join(map(lambda entry: str(round(entry, 2)), entry_list))
        all_ratios_for_entry = f'{independent_ratio_values}/{dependent_ratio_value}'
        return all_ratios_for_entry

    def _ratio_input_is_valid(self, min_max_values_with_increments):
        return True
