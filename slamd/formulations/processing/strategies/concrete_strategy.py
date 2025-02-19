import itertools
from typing import Literal

from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.constants import G_CM3_TO_KG_M3_CONVERSION_FACTOR
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.formulations.processing.models.formulation import Formulation, MaterialContent
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

        if selected_constraint_type == 'Volume':
            cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, 'Air-Pore-Content-1',
                                           'Air Pore Content', 'Air Pore Content')

        joined_aggregates_names = ', '.join(aggregates_names)
        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(aggregates_uuids),
                                       f'Aggregates ({joined_aggregates_names})', 'Aggregates')

        cls._create_process_fields(formulation_selection, min_max_form)

        min_max_form.liquid_info_entry.data = 'Liquids ({0})'.format(', '.join(liquid_names))

        return min_max_form

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        entry = cls._create_min_max_form_entry_internal(
            entries, uuids, name, material_type,
            ['Powder', 'Liquid', 'Aggregates'],
            ['Aggregates', 'Air Pore Content']
        )
        cls._populate_min_max_entry_with_default_values(entry, material_type)

    @classmethod
    def _populate_min_max_entry_with_default_values(cls, entry, type):
        if type == 'Powder':
            entry.increment.data = 10
            entry.min.data = 350
            entry.max.data = 450
        if type == 'Admixture':
            entry.increment.label.text = 'Increment (Admixture/Powder-ratio) %'
            entry.increment.data = 1
            entry.min.label.text = 'Min (Admixture/Powder-ratio) %'
            entry.min.data = 2
            entry.max.label.text = 'Max (Admixture/Powder-ratio) %'
            entry.max.data = 4
        if type == 'Air Pore Content':
            entry.increment.data = 0
            entry.increment.label.text = 'Increment %'
            entry.max.data = 2
            entry.max.label.text = 'Max %'
            entry.min.data = 2
            entry.min.label.text = 'Min %'
        if type == 'Custom':
            entry.increment.data = 5
            entry.min.data = 0
            entry.max.data = 20

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, constraint):
        return WeightsCalculator.compute_full_concrete_weights_product(all_materials_weights, constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)

    @classmethod
    def _create_preliminary_compositions(cls, combination, param_space):
        types = list(param_space.keys())

        compositions = []
        for composition in itertools.product(*[param_space[mt] for mt in types]):
            combination_dict = dict(zip(types, composition))

            compositions.append(
                Formulation(
                    powder=MaterialContent(
                        material=MaterialsFacade.get_material("powder", combination["Powder"]),
                        mass=combination_dict["Powder"],
                    ) if "Powder" in types else None,
                    liquid=MaterialContent(
                        material=MaterialsFacade.get_material("liquid", combination["Liquid"]),
                        mass=combination_dict["Liquid"] * combination_dict["Powder"] / 100,
                    ) if "Liquid" in types else None,
                    admixture=MaterialContent(
                        material=MaterialsFacade.get_material("admixture", combination["Admixture"]),
                        mass=combination_dict["Admixture"] * combination_dict["Powder"] / 100,
                    ) if "Admixture" in types else None,
                    custom=MaterialContent(
                        material=MaterialsFacade.get_material("custom", combination["Custom"]),
                        mass=combination_dict["Custom"],
                    ) if "Custom" in types else None,
                    air_pore_content=combination_dict["Air Pore Content"] if "Air Pore Content" in types else None,
                    process=MaterialsFacade.get_process(combination_dict["Process"]) if "Process" in types else None,
                    aggregate=MaterialContent(
                        material=MaterialsFacade.get_material("aggregates", combination["Aggregates"]),
                    ),
                )
            )

        return compositions

    @classmethod
    def _complete_composition(cls, f: Formulation, specific_gravities, constraint,
                              constraint_type: Literal["Volume", "Weight"]):
        total_volume = constraint * f.air_pore_content / 100 if f.air_pore_content is not None else 0
        f.total_mass = 0

        if f.powder:
            f.powder.volume = f.powder.mass / (
                    specific_gravities[str(f.powder.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += f.powder.volume
            f.total_mass += f.powder.mass

        if f.liquid:
            f.liquid.volume = f.liquid.mass / (
                    specific_gravities[str(f.liquid.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += f.liquid.volume
            f.total_mass += f.liquid.mass

        if f.admixture:
            f.admixture.volume = f.admixture.mass / (
                    specific_gravities[str(f.admixture.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += f.admixture.volume
            f.total_mass += f.admixture.mass

        if f.custom:
            f.custom.volume = f.custom.mass / (
                    specific_gravities[str(f.custom.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += f.custom.volume
            f.total_mass += f.custom.mass

        if constraint_type == "Volume" and total_volume > constraint:
            return None
        elif constraint_type == "Weight" and f.total_mass > constraint:
            return None

        if constraint_type == "Volume":
            f.aggregate.volume = constraint - total_volume
            f.aggregate.mass = round(
                f.aggregate.volume * specific_gravities[
                    str(f.aggregate.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2
            )
            f.total_mass += f.aggregate.mass
        elif constraint_type == "Weight":
            f.aggregate.mass = round(constraint - f.total_mass, 2)
            f.total_mass += f.aggregate.mass
        else:
            raise ValueError("Invalid constraint type: " + str(constraint_type))

        return f

    @classmethod
    def _create_dataframe(cls, formulations):
        return cls._create_dataframe_internal(formulations, TEMPORARY_CONCRETE_FORMULATION)
