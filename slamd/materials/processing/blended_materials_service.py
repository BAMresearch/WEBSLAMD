from itertools import product

from slamd.common.error_handling import MaterialNotFoundException, ValueNotSupportedException, \
    SlamdRequestTooLargeException
from slamd.common.slamd_utils import not_numeric
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.forms.ratio_form import RatioForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse

MAX_NUMBER_OF_RATIOS = 1000


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
        if not_numeric(count):
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

        if len(cartesian_product_list) > MAX_NUMBER_OF_RATIOS:
            raise SlamdRequestTooLargeException('Too many blends were requested. Try again with another configuration!')

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

    def _ratio_input_is_valid(self, min_max_increments_values):
        for i in range(len(min_max_increments_values)- 1):
            min_value = min_max_increments_values[i]['min']
            max_value = min_max_increments_values[i]['max']
            increment = min_max_increments_values[i]['increment']
            if self._validate_ranges(increment, max_value, min_value):
                return False
        return True

    def _validate_ranges(self, increment, max_value, min_value):
        return min_value < 0 or min_value > 100 or max_value > 100 or min_value > max_value \
               or max_value < 0 or increment <= 0 or not_numeric(max_value) \
               or not_numeric(min_value) or not_numeric(increment)
