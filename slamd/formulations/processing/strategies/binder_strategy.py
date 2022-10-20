from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_BINDER_FORMULATION
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.binder_selection_form import BinderSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.weights_calculator import WeightsCalculator
from slamd.materials.processing.materials_facade import MaterialsFacade


class BinderStrategy(BuildingMaterialStrategy):

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()
        form = cls._populate_common_ingredient_selection(BinderSelectionForm(), all_materials)
        return form

    @classmethod
    def get_formulations(cls):
        dataframe = None
        temporary_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_BINDER_FORMULATION)
        if temporary_dataset:
            dataframe = temporary_dataset.dataframe
        return dataframe

    @classmethod
    def create_min_max_form(cls, formulation_selection):
        powder_names = [item['name'] for item in formulation_selection if item['type'] == 'Powder']
        liquid_names = [item['name'] for item in formulation_selection if item['type'] == 'Liquid']
        aggregates_names = [item['name'] for item in formulation_selection if item['type'] == 'Aggregates']
        admixture_names = [item['name'] for item in formulation_selection if item['type'] == 'Admixture']
        custom_names = [item['name'] for item in formulation_selection if item['type'] == 'Custom']

        powder_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Powder']
        liquid_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Liquid']
        aggregates_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Aggregates']
        admixture_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Admixture']
        custom_uuids = [item['uuid'] for item in formulation_selection if item['type'] == 'Custom']

        if cls._check_for_invalid_material_lists(liquid_names, powder_names):
            raise ValueNotSupportedException('You need to specify at least one powder and one liquid')

        min_max_form = FormulationsMinMaxForm()

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(liquid_uuids),
                                       'W/C Ratio', 'Liquid')

        min_max_form.materials_min_max_entries.entries[-1].increment.label.text = 'Increment (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].min.label.text = 'Min (W/C-ratio)'
        min_max_form.materials_min_max_entries.entries[-1].max.label.text = 'Max (W/C-ratio)'

        if len(aggregates_names):
            joined_aggregates_names = ', '.join(aggregates_names)
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                           f'Aggregates ({joined_aggregates_names})', 'Aggregates')

        if len(admixture_names):
            joined_admixture_names = ', '.join(admixture_names)
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(admixture_uuids),
                                           f'Admixtures ({joined_admixture_names})', 'Admixture')

        if len(custom_names):
            joined_custom_names = ', '.join(custom_names)
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(custom_uuids),
                                           f'Customs ({joined_custom_names})', 'Custom')
        joined_powder_names = ', '.join(powder_names)
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(powder_uuids),
                                       f'Powders ({joined_powder_names})', 'Powder')

        cls._create_process_fields(formulation_selection, min_max_form)

        min_max_form.liquid_info_entry.data = 'Liquids ({0})'.format(', '.join(liquid_names))

        return min_max_form

    @classmethod
    def create_formulation_batch(cls, formulations_data):
        return cls._create_formulation_batch_internal(formulations_data, TEMPORARY_BINDER_FORMULATION)

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        cls._create_min_max_form_entry_internal(entries, uuids, name, material_type, ['Powder', 'Liquid'], 'Powder')

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, weight_constraint):
        return WeightsCalculator.compute_full_binder_weights_product(all_materials_weights, weight_constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_binder_formulation(materials_for_formulation)
