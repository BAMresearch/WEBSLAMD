from itertools import product

from slamd.common.common_validators import min_max_increment_config_valid
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.slamd_utils import not_numeric, not_empty, empty
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.ratio_parser import RatioParser

MAX_NUMBER_OF_WEIGHTS = 100


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
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.type.capitalize()}: {material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, count_materials, count_processes):
        if not_numeric(count_materials):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_processes) and not_numeric(count_processes):
            raise ValueNotSupportedException('Cannot process selection!')

        count_materials = int(count_materials)

        if not_empty(count_processes):
            count_processes = int(count_processes)

        if count_materials == 0:
            raise ValueNotSupportedException('No material selected!')

        min_max_form = FormulationsMinMaxForm()
        for i in range(count_materials):
            min_max_form.materials_min_max_entries.append_entry()

        for i in range(count_processes):
            min_max_form.processes_entries.append_entry()

        return min_max_form

    @classmethod
    def create_weights_form(cls, weights_request_data):
        material_configuration = weights_request_data['material_configuration']
        weight_constraint = weights_request_data['weight_constraint']

        if empty(weight_constraint):
            # TODO
            cls._create_unconstrained_weights(material_configuration)

        else:
            if not_numeric(weight_constraint):
                raise ValueNotSupportedException('Weight Constraint must be a number!')

            if not min_max_increment_config_valid(material_configuration, weight_constraint):
                raise ValueNotSupportedException('Configuration of weights is not valid!')

            for i in range(material_configuration):
                material_uuid = material_configuration['uuid']




            all_values = cls._prepare_values_for_cartesian_product(material_configuration)

            cartesian_product = product(*all_values)
            cartesian_product_list = list(cartesian_product)

            if len(cartesian_product_list) > MAX_NUMBER_OF_WEIGHTS:
                raise SlamdRequestTooLargeException(
                    f'Too many formulation configurations were requested. At most {MAX_NUMBER_OF_WEIGHTS} configurations can be created!')

            weigths_form = WeightsForm()
            for ratio_as_list in cartesian_product_list:
                all_ratios_for_entry = RatioParser.create_ratio_string(ratio_as_list)
                ratio_form_entry = weigths_form.all_ratio_entries.append_entry()
                ratio_form_entry.ratio.data = all_ratios_for_entry
            return weigths_form

    @classmethod
    def _create_unconstrained_weights(cls, min_max_values_with_increments):
        pass
