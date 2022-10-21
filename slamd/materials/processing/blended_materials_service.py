from itertools import product

from slamd.common.common_validators import min_max_increment_config_valid
from slamd.common.error_handling import MaterialNotFoundException, ValueNotSupportedException, \
    SlamdRequestTooLargeException
from slamd.common.slamd_utils import not_numeric
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.blending_name_and_type_form import BlendingNameAndTypeForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.forms.ratio_form import RatioForm
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.materials_service import MaterialsService, MaterialsResponse

RATIO_DELIMITER = '/'
MAX_NUMBER_OF_RATIOS = 100


class BlendedMaterialsService(MaterialsService):

    @classmethod
    def create_materials_response(cls, materials):
        return MaterialsResponse(materials, 'blended materials')

    @classmethod
    def list_base_material_selection_by_type(cls, material_type):
        material_type = material_type.lower()
        if material_type not in MaterialType.get_all_types():
            raise MaterialNotFoundException(f'The requested type "{material_type}" is not supported!')

        materials_by_type = MaterialsPersistence.query_by_type(material_type)
        material_selection = [(material.uuid, material.name)
                              for material in materials_by_type if material.is_blended is False]

        sorted_by_name = sorted(material_selection, key=lambda material: material[1])
        form = BaseMaterialSelectionForm()
        form.base_material_selection.choices = sorted_by_name
        return form

    @classmethod
    def create_min_max_form(cls, material_type, count, base_material_uuids):
        if not_numeric(count):
            raise ValueNotSupportedException('Cannot process selection!')

        count = int(count)

        if count < 2:
            raise ValueNotSupportedException('At least two items must be selected!')

        selected_base_materials_as_dict = []
        for uuid in base_material_uuids:
            material = MaterialsPersistence.query_by_type_and_uuid(material_type, uuid)
            selected_base_materials_as_dict.append(material.__dict__)

        strategy = MaterialFactory.create_strategy(material_type)
        complete = strategy.check_completeness_of_base_material_properties(selected_base_materials_as_dict)

        min_max_form = MinMaxForm()
        for _ in range(count):
            min_max_form.all_min_max_entries.append_entry()

        # Min/Max of the last entry are calculated from the previous entries, and the labels need to be switched
        min_max_form.all_min_max_entries[-1].min.label.text = 'Max (%)'
        min_max_form.all_min_max_entries[-1].max.label.text = 'Min (%)'

        return min_max_form, complete

    @classmethod
    def delete_material(cls, material_type, uuid):
        MaterialsPersistence.delete_by_type_and_uuid(material_type, uuid)
        return cls.list_materials(blended=True)

    @classmethod
    def create_ratio_form(cls, min_max_values_with_increments):
        if not min_max_increment_config_valid(min_max_values_with_increments, 100):
            raise ValueNotSupportedException('Configuration of ratios is not valid!')

        all_values = cls._prepare_values_for_cartesian_product(min_max_values_with_increments)

        cartesian_product = product(*all_values)
        cartesian_product_list = list(cartesian_product)

        if len(cartesian_product_list) > MAX_NUMBER_OF_RATIOS:
            raise SlamdRequestTooLargeException(
                f'Too many blends were requested. At most {MAX_NUMBER_OF_RATIOS} ratios can be created!')

        ratio_form = RatioForm()
        for ratio_as_list in cartesian_product_list:
            all_ratios_for_entry = RatioParser.create_ratio_string(ratio_as_list)
            ratio_form_entry = ratio_form.all_ratio_entries.append_entry()
            ratio_form_entry.ratio.data = all_ratios_for_entry
        return ratio_form

    @classmethod
    def save_blended_materials(cls, submitted_blending_configuration):
        all_ratios_as_string, base_material_uuids = cls._validate_configuration(submitted_blending_configuration)

        base_materials_as_dict = []
        base_type = submitted_blending_configuration['base_type']

        for base_material_uuid in base_material_uuids:
            base_material = MaterialsPersistence.query_by_type_and_uuid(base_type, base_material_uuid)
            if base_material is None:
                raise MaterialNotFoundException('The requested base materials do no longer exist!')
            base_materials_as_dict.append(base_material.__dict__)

        list_of_normalized_ratios_lists = RatioParser.create_list_of_normalized_ratio_lists(all_ratios_as_string,
                                                                                            RATIO_DELIMITER)

        strategy = MaterialFactory.create_strategy(base_type.lower())

        for ratio_list in list_of_normalized_ratios_lists:
            if len(ratio_list) != len(base_materials_as_dict):
                raise ValueNotSupportedException('Ratios cannot be matched with base materials!')

            blend_name = submitted_blending_configuration['blended_material_name']
            blended_material_name = f'{blend_name}-{RatioParser.ratio_list_to_ratio_string(ratio_list)}'
            blended_material = strategy.create_blended_material(blended_material_name, ratio_list,
                                                                base_materials_as_dict)
            strategy.save_model(blended_material)

    @classmethod
    def _validate_configuration(cls, submitted_blending_configuration):
        blending_name_any_type_form = BlendingNameAndTypeForm(submitted_blending_configuration)
        if not blending_name_any_type_form.validate():
            raise ValueNotSupportedException('The blending name is empty or already used!')

        all_ratios_as_string = [value for key, value in submitted_blending_configuration.items() if
                                'all_ratio_entries-' in key]
        if len(all_ratios_as_string) > MAX_NUMBER_OF_RATIOS:
            raise SlamdRequestTooLargeException(
                f'Too many ratios were passed! At most {MAX_NUMBER_OF_RATIOS} can be processed!')

        base_material_uuids = submitted_blending_configuration.getlist('base_material_selection')
        if not cls._ratios_are_valid(all_ratios_as_string, len(base_material_uuids)):
            raise ValueNotSupportedException('There are invalid ratios. Make sure they satisfy the correct pattern!')

        return all_ratios_as_string, base_material_uuids

    @classmethod
    def _prepare_values_for_cartesian_product(cls, min_max_values_with_increments):
        all_values = []
        for i in range(len(min_max_values_with_increments) - 1):
            values_for_given_base_material = []
            current_value = min_max_values_with_increments[i]['min']
            max_value = min_max_values_with_increments[i]['max']
            increment = min_max_values_with_increments[i]['increment']
            while current_value <= max_value:
                values_for_given_base_material.append(current_value)
                current_value += increment
            all_values.append(values_for_given_base_material)
        return all_values

    @classmethod
    def _ratios_are_valid(cls, all_ratios, number_of_base_materials):
        for ratio in all_ratios:
            pieces_of_a_ratio = ratio.split(RATIO_DELIMITER)
            if len(pieces_of_a_ratio) != number_of_base_materials:
                return False
            for pieces_of_a_ratio in pieces_of_a_ratio:
                if not_numeric(pieces_of_a_ratio):
                    return False
        return True
