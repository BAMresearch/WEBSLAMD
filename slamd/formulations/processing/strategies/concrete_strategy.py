from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.concrete_selection_form import ConcreteSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.volumes_calculator import VolumesCalculator
from slamd.formulations.processing.weight_input_preprocessor import WeightInputPreprocessor
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade
from itertools import product

MAX_DATASET_SIZE = 10000


class ConcreteStrategy(BuildingMaterialStrategy):

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()
        form = cls._populate_common_ingredient_selection(ConcreteSelectionForm(), all_materials)
        return form

    @classmethod
    def get_formulations(cls):
        dataframe = None
        temporary_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)
        if temporary_dataset:
            dataframe = temporary_dataset.dataframe
        return dataframe

    @classmethod
    def create_min_max_form(cls, formulation_selection, selected_constraint_type):
        result = cls.classify_formulation_selection(formulation_selection)
        powder_names, powder_uuids = result['Powder']
        liquid_names, liquid_uuids = result['Liquid']
        aggregates_names, aggregates_uuids = result['Aggregates']
        admixture_names, admixture_uuids = result['Admixture']
        custom_names, custom_uuids = result['Custom']

        if cls._check_for_invalid_material_lists(aggregates_names, liquid_names, powder_names):
            raise ValueNotSupportedException('You need to specify at least one powder, liquid and aggregate')

        min_max_form = FormulationsMinMaxForm()

        joined_powder_names = ', '.join(powder_names)
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(powder_uuids),
                                       f'Powders ({joined_powder_names})', 'Powder')
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(liquid_uuids),
                                       'W/C Ratio', 'Liquid')

        min_max_form.materials_min_max_entries.entries[-1].increment.label.text = 'Increment (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].increment.data = 5
        min_max_form.materials_min_max_entries.entries[-1].min.label.text = 'Min (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].min.data = 35
        min_max_form.materials_min_max_entries.entries[-1].max.label.text = 'Max (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].max.data = 60




        if len(admixture_names):
            joined_admixture_names = ', '.join(admixture_names)
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(admixture_uuids),
                                           f'Admixtures ({joined_admixture_names})', 'Admixture')

        if len(custom_names):
            joined_custom_names = ', '.join(custom_names)
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(custom_uuids),
                                           f'Customs ({joined_custom_names})', 'Custom')

        if selected_constraint_type == 'Volume':
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, 'Air-Pore-Content-1', 'Air Pore Content', 'Air Pore Content')

        joined_aggregates_names = ', '.join(aggregates_names)
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                       f'Aggregates ({joined_aggregates_names})', 'Aggregates')

        cls._create_process_fields(formulation_selection, min_max_form)

        min_max_form.liquid_info_entry.data = 'Liquids ({0})'.format(', '.join(liquid_names))

        return min_max_form

    @classmethod
    def create_formulation_batch(cls, formulations_data):
        return cls._create_formulation_batch_internal(formulations_data, TEMPORARY_CONCRETE_FORMULATION)

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        cls._create_min_max_form_entry_internal(entries, uuids, name, material_type, ['Powder', 'Liquid', 'Aggregates'],
                                                ['Aggregates', 'Air Pore Content'])

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, weight_constraint):
        return WeightsCalculator.compute_full_concrete_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)

    @classmethod
    def generate_formulations_with_weights_for_volume_constraint(cls, min_max_data, specific_gravities):
        materials_weights_and_ratios = WeightInputPreprocessor.collect_weights(min_max_data['materials_formulation_configuration'])

        materials_in_formulation = [material.get('type') for material in min_max_data['materials_formulation_configuration']]

        admixture_and_custom_materials_indices = cls._calculate_admixture_and_custom_indices(materials_in_formulation)

        material_weights = WeightsCalculator.compute_weights_from_ratios(materials_weights_and_ratios, admixture_and_custom_materials_indices)

        material_volumes = VolumesCalculator.compute_volumes_from_weights(material_weights, specific_gravities, admixture_and_custom_materials_indices)

        material_combinations = cls._generate_material_combinations(material_volumes)

        material_volumes_for_all_combinations = VolumesCalculator.generate_volumes_for_combinations(material_combinations)

        valid_volumes_for_all_combinations = VolumesCalculator.validate_volume_combinations(material_volumes_for_all_combinations, min_max_data['weight_constraint'])

        valid_formulations_with_aggregates = VolumesCalculator.add_aggregates_volume_to_combination(valid_volumes_for_all_combinations, specific_gravities, min_max_data['weight_constraint'])

        formulations_with_weights = VolumesCalculator.transform_volumes_to_weights(valid_formulations_with_aggregates, specific_gravities, admixture_and_custom_materials_indices)

        return formulations_with_weights

    @classmethod
    def _generate_material_combinations(cls, all_material_volumes):
        powders = [material for material in all_material_volumes if material['type'] == 'Powder']
        liquids = [material for material in all_material_volumes if material['type'] == 'Liquid']
        admixtures = [material for material in all_material_volumes if material['type'] == 'Admixture']
        customs = [material for material in all_material_volumes if material['type'] == 'Custom']

        if admixtures and customs:
            formulation_list = [
                [powder, liquid, admixture, custom]
                for powder, liquid, admixture, custom in product(powders, liquids, admixtures, customs)
            ]
        elif admixtures and not customs:
            formulation_list = [
                [powder, liquid, admixture]
                for powder, liquid, admixture in product(powders, liquids, admixtures)
            ]
        elif customs and not admixtures:
            formulation_list = [
                [powder, liquid, customs]
                for powder, liquid, customs in product(powders, liquids, customs)
            ]
        else:
            formulation_list = [
                [powder, liquid]
                for powder, liquid in product(powders, liquids)
            ]

        return formulation_list

    @classmethod
    def _calculate_admixture_and_custom_indices(cls, materials_in_formulation):
        admixture_index = None
        custom_index = None
        if 'Admixture' in materials_in_formulation and 'Custom' not in materials_in_formulation:
            admixture_index = 2
        if 'Custom' in materials_in_formulation and 'Admixture' not in materials_in_formulation:
            custom_index = 2
        if 'Admixture' in materials_in_formulation and 'Custom' in materials_in_formulation:
            admixture_index = 2
            custom_index = 3
        indices = {'admixture_index': admixture_index, 'custom_index': custom_index}
        return indices
