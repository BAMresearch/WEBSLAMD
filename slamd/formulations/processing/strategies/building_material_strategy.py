import itertools
from abc import ABC, abstractmethod
from typing import Literal

import pandas as pd

from slamd.common.common_validators import validate_ranges
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.common.slamd_utils import empty, not_numeric
from slamd.discovery.processing.discovery_facade import DiscoveryFacade
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.models.formulation import Formulation
from slamd.formulations.processing.weight_input_preprocessor import MAX_NUMBER_OF_WEIGHTS, WeightInputPreprocessor
from slamd.materials.processing.materials_facade import MaterialsFacade

WEIGHT_FORM_DELIMITER = '/'
MAX_DATASET_SIZE = 10000


class BuildingMaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_min_max_form(cls, formulation_selection, selected_constraint_type):
        pass

    @classmethod
    @abstractmethod
    def populate_selection_form(cls):
        pass

    @classmethod
    @abstractmethod
    def get_formulations(cls):
        pass

    @classmethod
    def classify_formulation_selection(cls, formulation_selection):
        powder_names = []
        liquid_names = []
        aggregates_names = []
        admixture_names = []
        custom_names = []
        powder_uuids = []
        liquid_uuids = []
        aggregates_uuids = []
        admixture_uuids = []
        custom_uuids = []
        # Classify the selection in a single pass.
        # Separate names and uuids.
        for item in formulation_selection:
            if item['type'] == 'Powder':
                powder_names.append(item['name'])
                powder_uuids.append(item['uuid'])
            if item['type'] == 'Liquid':
                liquid_names.append(item['name'])
                liquid_uuids.append(item['uuid'])
            if item['type'] == 'Aggregates':
                aggregates_names.append(item['name'])
                aggregates_uuids.append(item['uuid'])
            if item['type'] == 'Admixture':
                admixture_names.append(item['name'])
                admixture_uuids.append(item['uuid'])
            if item['type'] == 'Custom':
                custom_names.append(item['name'])
                custom_uuids.append(item['uuid'])
        return {
            'Powder': (powder_names, powder_uuids),
            'Liquid': (liquid_names, liquid_uuids),
            'Aggregates': (aggregates_names, aggregates_uuids),
            'Admixture': (admixture_names, admixture_uuids),
            'Custom': (custom_names, custom_uuids)
        }

    @classmethod
    def populate_weights_form(cls, weights_request_data):
        materials_formulation_config = weights_request_data['materials_formulation_configuration']
        constraint = weights_request_data["constraint"]

        # the result of the computation contains a list of lists with each containing the weights in terms of the
        # various materials used for blending; for example weight_combinations =
        # "[['18.2', '15.2', '66.6'], ['18.2', '20.3', '61.5'], ['28.7', '15.2', '56.1']]"
        if empty(constraint):
            raise ValueNotSupportedException('You must set a non-empty weight constraint!')
        else:
            weight_combinations = cls._get_constrained_weights(materials_formulation_config, constraint)

        if len(weight_combinations) > MAX_NUMBER_OF_WEIGHTS:
            raise SlamdRequestTooLargeException(
                f'Too many weights were requested. At most {MAX_NUMBER_OF_WEIGHTS} weights can be created!')

        weights_form = WeightsForm()
        for i, entry in enumerate(weight_combinations):
            ratio_form_entry = weights_form.all_weights_entries.append_entry()
            ratio_form_entry.weights.data = WEIGHT_FORM_DELIMITER.join(entry)
            ratio_form_entry.idx.data = str(i)
        return weights_form

    @classmethod
    @abstractmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, type):
        pass

    @classmethod
    def _populate_common_ingredient_selection(cls, form, all_materials):
        form.powder_selection.choices = cls._to_selection(all_materials.powders)
        form.liquid_selection.choices = cls._to_selection(all_materials.liquids)
        form.aggregates_selection.choices = cls._to_selection(all_materials.aggregates_list)
        form.admixture_selection.choices = cls._to_selection(all_materials.admixtures)
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)
        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return [(f'{material.type}|{str(material.uuid)}', f'{material.name}') for material in by_type]

    @classmethod
    def _check_for_invalid_material_lists(cls, *material_lists):
        for material_list in material_lists:
            if len(material_list) == 0:
                return True
        return False

    @classmethod
    def _create_process_fields(cls, formulation_selection, min_max_form):
        selection_for_type = [item for item in formulation_selection if item['type'] == 'Process']
        for item in selection_for_type:
            cls._create_min_max_form_entry(min_max_form.process_entries, item['uuid'], item['name'], 'Process')

    @classmethod
    def _get_constrained_weights(cls, formulation_config, constraint):
        if not_numeric(constraint):
            raise ValueNotSupportedException('Weight Constraint must be a number!')
        if not cls._weight_ranges_valid(formulation_config, constraint):
            raise ValueNotSupportedException('Configuration of weights is not valid!')

        all_materials_weights = WeightInputPreprocessor.collect_weights(formulation_config)

        return cls._compute_weights_product(all_materials_weights, constraint)

    @classmethod
    @abstractmethod
    def _compute_weights_product(cls, all_materials_weights, constraint):
        pass

    @classmethod
    def _weight_ranges_valid(cls, formulation_config, constraint):
        # Skip aggregate (last value)
        for i, conf in enumerate(formulation_config[:-1]):
            if i == 1:
                # liquid - ratios, calculate differently
                min_value = float(conf['min']) * float(formulation_config[0]['min'])
                max_value = float(conf['max']) * float(formulation_config[0]['max'])
                # validation checks if increment is negative, 0 or non_numeric - does not need to be multiplied
                increment = float(conf['increment'])
            else:
                # everything else - regular validation
                min_value = float(conf['min'])
                max_value = float(conf['max'])
                increment = float(conf['increment'])

            if validate_ranges(increment, max_value, min_value, float(constraint)):
                return False

        return True

    @classmethod
    @abstractmethod
    def _sort_materials(cls, materials_for_formulation):
        pass

    @classmethod
    def _create_min_max_form_entry_internal(cls, entries, uuids, name, type, req_types, disabled_type):
        entry = entries.append_entry()
        entry.materials_entry_name.data = name
        entry.uuid_field.data = uuids
        entry.type_field.data = type
        if type in req_types:
            entry.increment.name = type
            entry.min.name = type
            entry.max.name = type
        if type in disabled_type:
            entry.increment.render_kw = {'disabled': 'disabled'}
            entry.min.render_kw = {'disabled': 'disabled'}
            entry.max.render_kw = {'disabled': 'disabled'}
            entry.min.label.text = 'Max (kg)'
            entry.max.label.text = 'Min (kg)'

        return entry

    @classmethod
    def generate_formulations(cls, min_max_data, constraint, constraint_type: Literal["Volume", "Weight"], processes):
        materials = cls._extract_material_uuids(min_max_data)
        material_and_process_combinations = cls._find_material_and_process_combinations(
            {**materials, "Process": processes} if processes else materials
        )

        weights_and_ratios = WeightInputPreprocessor.collect_weights_as_dict(min_max_data)
        parameter_space = {**weights_and_ratios, "Process": processes} if processes else weights_and_ratios

        compositions = []
        for combination in material_and_process_combinations:
            compositions.extend(
                cls._create_preliminary_compositions(combination, parameter_space)
            )

        specific_gravities = cls._get_specific_gravities(materials)

        completed_compositions = []
        for composition in compositions:
            if completed_composition := cls._complete_composition(composition, specific_gravities, constraint,
                                                                  constraint_type):
                cls._calculate_composition_cost(completed_composition)
                completed_compositions.append(completed_composition)

        return cls._create_dataframe(completed_compositions)

    @classmethod
    def _extract_material_uuids(cls, min_max_data):
        result = {}
        for item in min_max_data:
            material_type = item['type']
            uuids = item['uuid'].split(',')

            if material_type not in result:
                result[material_type] = []

            result[material_type].extend(uuids)

        return result

    @classmethod
    def _find_material_and_process_combinations(cls, type_to_uuids):
        types = list(type_to_uuids.keys())
        uuid_lists = [type_to_uuids[material_type] for material_type in types]

        raw_combinations = itertools.product(*uuid_lists)

        combinations = []
        for combination in raw_combinations:
            combination_dict = {t: uuid for t, uuid in zip(types, combination)}
            combinations.append(combination_dict)

        return combinations

    @classmethod
    @abstractmethod
    def _create_preliminary_compositions(cls, combination, param_space):
        pass

    @classmethod
    def _get_specific_gravities(cls, materials_dict):
        densities_dict = {}
        for material, uuids in materials_dict.items():
            if material == "Air Pore Content":
                continue

            for uuid in uuids:
                session_value = MaterialsFacade.get_material_from_session(material, uuid)
                densities_dict[uuid] = float(session_value.specific_gravity)

        return densities_dict

    @classmethod
    @abstractmethod
    def _complete_composition(cls, f: Formulation, specific_gravities, constraint,
                              constraint_type: Literal["Volume", "Weight"]):
        pass

    @classmethod
    def _calculate_composition_cost(cls, f: Formulation):
        f.costs = 0
        f.co2_footprint = 0
        f.delivery_time = 0
        f.recycling_rate = 0

        if f.powder:
            powder_factor = f.powder.mass / f.total_mass
            f.costs += (f.powder.material.costs.costs or 0) * powder_factor
            f.co2_footprint += (f.powder.material.costs.co2_footprint or 0) * powder_factor
            f.recycling_rate += (f.powder.material.costs.recyclingrate or 0) * powder_factor
            f.delivery_time = max(f.delivery_time, f.powder.material.costs.delivery_time or 0)

        if f.liquid:
            liquid_factor = f.liquid.mass / f.total_mass
            f.costs += (f.liquid.material.costs.costs or 0) * liquid_factor
            f.co2_footprint += (f.liquid.material.costs.co2_footprint or 0) * liquid_factor
            f.recycling_rate += (f.liquid.material.costs.recyclingrate or 0) * liquid_factor
            f.delivery_time = max(f.delivery_time, f.liquid.material.costs.delivery_time or 0)

        if f.admixture:
            admixture_factor = f.admixture.mass / f.total_mass
            f.costs += (f.admixture.material.costs.costs or 0) * admixture_factor
            f.co2_footprint += (f.admixture.material.costs.co2_footprint or 0) * admixture_factor
            f.recycling_rate += (f.admixture.material.costs.recyclingrate or 0) * admixture_factor
            f.delivery_time = max(f.delivery_time, f.admixture.material.costs.delivery_time or 0)

        if f.custom:
            custom_factor = f.custom.mass / f.total_mass
            f.costs += (f.custom.material.costs.costs or 0) * custom_factor
            f.co2_footprint += (f.custom.material.costs.co2_footprint or 0) * custom_factor
            f.recycling_rate += (f.custom.material.costs.recyclingrate or 0) * custom_factor
            f.delivery_time = max(f.delivery_time, f.custom.material.costs.delivery_time or 0)

        if f.aggregate:
            aggregate_factor = f.aggregate.mass / f.total_mass
            f.costs += (f.aggregate.material.costs.costs or 0) * aggregate_factor
            f.co2_footprint += (f.aggregate.material.costs.co2_footprint or 0) * aggregate_factor
            f.recycling_rate += (f.aggregate.material.costs.recyclingrate or 0) * aggregate_factor
            f.delivery_time = max(f.delivery_time, f.aggregate.material.costs.delivery_time or 0)

        if f.process:
            f.costs += f.process.costs.costs or 0
            f.co2_footprint += f.process.costs.co2_footprint or 0
            f.delivery_time = max(f.delivery_time, f.process.costs.delivery_time or 0)

        f.costs = round(f.costs, 2)
        f.co2_footprint = round(f.co2_footprint, 2)
        f.delivery_time = round(f.delivery_time, 2)
        f.recycling_rate = round(f.recycling_rate, 2)

    @classmethod
    @abstractmethod
    def _create_dataframe(cls, formulations):
        pass

    @classmethod
    def _create_dataframe_internal(cls, formulations, filename):
        rows = []
        for idx, formulation in enumerate(formulations):
            row = {
                'Idx_Sample': idx,
                'Powder (kg)': formulation.powder.mass,
                'Liquid (kg)': formulation.liquid.mass,
                'Aggregates (kg)': formulation.aggregate.mass if formulation.aggregate else None,
                'Admixture (kg)': formulation.admixture.mass if formulation.admixture else None,
                f'{formulation.custom.material.name} (kg)' if formulation.custom else "__placeholder": formulation.custom.mass if formulation.custom else None,
                'Materials': ", ".join(filter(None, [
                    formulation.powder.material.name if formulation.powder else None,
                    formulation.liquid.material.name if formulation.liquid else None,
                    formulation.admixture.material.name if formulation.admixture else None,
                    formulation.custom.material.name if formulation.custom else None,
                    formulation.aggregate.material.name if formulation.aggregate else None,
                    formulation.process.name if formulation.process else None,
                ])),
                'total costs': formulation.costs,
                'total co2_footprint': formulation.co2_footprint,
                'total delivery_time': formulation.delivery_time,
                'total recycling_rate': formulation.recycling_rate,
            }
            rows.append(row)

        df = pd.DataFrame(rows).dropna(axis="columns", how="all")
        if previous_batch_df := DiscoveryFacade.query_dataset_by_name(filename):
            df = pd.concat((previous_batch_df.dataframe, df))

        df["Idx_Sample"] = range(0, len(df))
        df.insert(0, "Idx_Sample", df.pop("Idx_Sample"))

        temp_dataset = Dataset(name=filename, dataframe=df)
        DiscoveryFacade.save_and_overwrite_dataset(temp_dataset, filename)

        return df
