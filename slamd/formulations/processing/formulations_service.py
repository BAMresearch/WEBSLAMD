from slamd.common.common_validators import min_max_increment_config_valid
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.slamd_utils import not_numeric, not_empty, empty
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_converter import FormulationsConverter
from slamd.formulations.processing.formulations_dto import FormulationsDto
from slamd.formulations.processing.formulations_persistence import FormulationsPersistence
from slamd.formulations.processing.weight_input_preprocessor import WeightInputPreprocessor
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade

WEIGHT_FORM_DELIMITER = '  |  '
MAX_NUMBER_OF_WEIGHTS = 100


class FormulationsService:

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()

        form = MaterialsAndProcessesSelectionForm()
        form.powder_selection.choices.extend(cls._to_selection(all_materials.powders))
        form.liquid_selection.choices.extend(cls._to_selection(all_materials.liquids))
        form.aggregates_selection.choices.extend(cls._to_selection(all_materials.aggregates_list))
        form.admixture_selection.choices.extend(cls._to_selection(all_materials.admixtures))
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)

        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.name}'), by_type))

    @classmethod
    def create_formulations_min_max_form(cls, count_materials, count_processes):
        if not_empty(count_materials) and not_numeric(count_materials):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_processes) and not_numeric(count_processes):
            raise ValueNotSupportedException('Cannot process selection!')

        if not_empty(count_materials):
            count_materials = int(count_materials)

        if not_empty(count_processes):
            count_processes = int(count_processes)

        min_max_form = FormulationsMinMaxForm()
        for i in range(count_materials):
            min_max_form.materials_min_max_entries.append_entry()

        for i in range(count_processes):
            min_max_form.processes_entries.append_entry()

        return min_max_form

    @classmethod
    def create_weights_form(cls, weights_request_data):
        materials_formulation_config = weights_request_data['materials_formulation_configuration']
        weight_constraint = weights_request_data['weight_constraint']

        # the result of the computation contains a list of lists with each containing the weights in terms of the
        # base materials; for example full_cartesian_product =
        # "[['3.64/14.56', '15.2', '66.6'], ['3.64/14.56', '20.3', '61.5'], ['5.74/22.96', '15.2', '56.1']]"
        if empty(weight_constraint):
            full_cartesian_product, all_names = cls._get_unconstrained_base_weights(materials_formulation_config)
        else:
            full_cartesian_product, all_names = cls._get_constrained_base_weights(materials_formulation_config,
                                                                                  weight_constraint)
        if len(full_cartesian_product) > MAX_NUMBER_OF_WEIGHTS:
            raise SlamdRequestTooLargeException(
                f'Too many weights were requested. At most {MAX_NUMBER_OF_WEIGHTS} weights can be created!')

        weights_form = WeightsForm()
        for i, entry in enumerate(full_cartesian_product):
            ratio_form_entry = weights_form.all_weights_entries.append_entry()
            ratio_form_entry.weights.data = WEIGHT_FORM_DELIMITER.join(entry)
            ratio_form_entry.idx.data = str(i)
        base_names = WEIGHT_FORM_DELIMITER.join(all_names)
        return weights_form, base_names.strip()

    @classmethod
    def _get_constrained_base_weights(cls, formulation_config, weight_constraint):
        if not_numeric(weight_constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not min_max_increment_config_valid(formulation_config, weight_constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights, all_names = WeightInputPreprocessor.collect_base_names_and_weights(formulation_config)

        full_cartesian_product = WeightsCalculator.compute_full_cartesian_product(all_materials_weights,
                                                                                  formulation_config,
                                                                                  weight_constraint)
        return full_cartesian_product, all_names

    @classmethod
    def _get_unconstrained_base_weights(cls, formulation_config):
        if not cls._unconstrained_min_max_increment_config_valid(formulation_config):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights, all_names = WeightInputPreprocessor.collect_base_names_and_weights(formulation_config,
                                                                                                  False)
        full_cartesian_product = WeightsCalculator.compute_cartesian_product(all_materials_weights)
        return full_cartesian_product, all_names

    @classmethod
    def _unconstrained_min_max_increment_config_valid(cls, materials_formulation_configuration):
        for i in range(len(materials_formulation_configuration) - 1):
            min_value = float(materials_formulation_configuration[i]['min'])
            max_value = float(materials_formulation_configuration[i]['max'])
            increment = float(materials_formulation_configuration[i]['increment'])
            if cls._validate_unconstrained_ranges(increment, max_value, min_value):
                return False
        return True

    @classmethod
    def _validate_unconstrained_ranges(cls, increment, max_value, min_value):
        return min_value < 0 or min_value > max_value or max_value < 0 or increment <= 0 or not_numeric(max_value) \
               or not_numeric(min_value) or not_numeric(increment)

    # TODO: Implement constraint case / validate pattern of targets
    @classmethod
    def create_materials_formulations(cls, formulations_data):
        materials_data = formulations_data['materials_request_data']['materials_formulation_configuration']
        weigth_constraint = formulations_data['materials_request_data']['weight_constraint']
        processes_data = formulations_data['processes_request_data']['processes']
        targets = formulations_data['targets']

        all_weights = []
        if empty(weigth_constraint):
            all_weights = WeightInputPreprocessor.collect_weights_for_creation_of_formulation_batch(materials_data)
        weight_product = WeightsCalculator.compute_cartesian_product(all_weights)

        materials = []
        for material_data in materials_data:
            materials.append(MaterialsFacade.get_material(material_data['type'], material_data['uuid']))

        processes = []
        for process in processes_data:
            processes.append(MaterialsFacade.get_process(process['uuid']))

        dataframe = FormulationsConverter.formulation_to_df(materials, processes, weight_product, targets)
        # dataframe.to_csv('./test_slamd.csv')
        FormulationsPersistence.save(dataframe)

        as_dict = dataframe.transpose().to_dict()

        all_dtos = []
        for key, inner_dict in as_dict.items():
            properties = cls._create_properties(inner_dict, targets)
            target_list = cls._create_targets(inner_dict, targets)
            dto = FormulationsDto(properties=properties, targets=target_list)
            all_dtos.append(dto)
        return dataframe, all_dtos, targets.split(';')

    @classmethod
    def _create_properties(cls, inner_dict, targets):
        properties = ''
        target_list = targets.split(';')
        properties_dict = {k: v for k, v in inner_dict.items() if k not in target_list}
        for key, value in properties_dict.items():
            properties += f'{key}: {value}; '
        properties = properties.strip()[:-1]
        return properties

    @classmethod
    def _create_targets(cls, inner_dict, targets):
        targets_as_dto = []
        target_list = targets.split(';')
        target_dict = {k: v for k, v in inner_dict.items() if k in target_list}
        for key, value in target_dict.items():
            targets_as_dto.append(value)
        return targets_as_dto
