from functools import reduce

from slamd.common.error_handling import MaterialNotFoundException, ValueNotSupportedException
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.forms.ratio_form import RatioForm, RatioEntriesForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from itertools import product


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
        if not count.isnumeric():
            raise ValueNotSupportedException('Cannot process selection!')

        min_max_form = MinMaxForm()
        for i in range(int(count)):
            min_max_form.all_min_max_entries.append_entry()
        return min_max_form

    def create_ratio_form(self, min_max_values_with_increments):
        all_values = []
        for i in range(len(min_max_values_with_increments) - 1):
            values_for_given_base_material = []
            current_value = min_max_values_with_increments[i]['min']
            max = min_max_values_with_increments[i]['max']
            increment = min_max_values_with_increments[i]['increment']
            while current_value <= max:
                values_for_given_base_material.append(current_value)
                current_value += increment
            all_values.append(values_for_given_base_material)

        cartesian_product = product(*all_values)
        cartesian_product_list = list(cartesian_product)

        all_ratios = []
        ratio_form = RatioForm()
        for entry in cartesian_product_list:
            entry_list = list(entry)
            sum_of_independent_ratios = reduce(lambda x, y: x + y, entry_list)
            dependent_ratio_value = 100 - sum_of_independent_ratios
            independent_ratio_values = "/".join(map(lambda entry: str(entry), entry_list))
            all_ratios_for_entry = f'{independent_ratio_values}/{dependent_ratio_value}'
            ratio_form_entry = ratio_form.all_ratio_entries.append_entry()
            ratio_form_entry.ratio.data = all_ratios_for_entry
            #all_ratios.append(all_ratios_for_entry)
        return ratio_form


