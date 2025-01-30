from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.concrete_selection_form import ConcreteSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade

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

        joined_aggregates_names = ', '.join(aggregates_names)
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                       f'Aggregates ({joined_aggregates_names})', 'Aggregates')

        if selected_constraint_type == 'Volume':
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, 'Air-Void-Content-1', 'Air Void Contents', 'Air Void Content')

        cls._create_process_fields(formulation_selection, min_max_form)

        min_max_form.liquid_info_entry.data = 'Liquids ({0})'.format(', '.join(liquid_names))

        return min_max_form

    @classmethod
    def create_formulation_batch(cls, formulations_data):
        return cls._create_formulation_batch_internal(formulations_data, TEMPORARY_CONCRETE_FORMULATION)

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        cls._create_min_max_form_entry_internal(entries, uuids, name, material_type, ['Powder', 'Liquid', 'Aggregates'],
                                                'Aggregates')

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, weight_constraint):
        return WeightsCalculator.compute_full_concrete_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)
