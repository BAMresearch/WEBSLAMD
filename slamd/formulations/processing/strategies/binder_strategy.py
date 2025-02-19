import itertools
from typing import Literal

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_BINDER_FORMULATION
from slamd.formulations.processing.models.formulation import Formulation, MaterialContent
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.binder_selection_form import BinderSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
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
    def create_min_max_form(cls, formulation_selection, selected_constraint_type):
        result = cls.classify_formulation_selection(formulation_selection)
        powder_names, powder_uuids = result['Powder']
        liquid_names, liquid_uuids = result['Liquid']
        aggregates_names, aggregates_uuids = result['Aggregates']
        admixture_names, admixture_uuids = result['Admixture']
        custom_names, custom_uuids = result['Custom']

        if cls._check_for_invalid_material_lists(liquid_names, powder_names):
            raise ValueNotSupportedException('You need to specify at least one powder and one liquid')

        min_max_form = FormulationsMinMaxForm()

        cls._create_min_max_form_entry(min_max_form.materials_min_max_entries, ','.join(liquid_uuids),
                                       'W/C Ratio', 'Liquid')

        min_max_form.materials_min_max_entries.entries[-1].increment.label.text = 'Increment (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].increment.data = 5
        min_max_form.materials_min_max_entries.entries[-1].min.label.text = 'Min (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].min.data = 35
        min_max_form.materials_min_max_entries.entries[-1].max.label.text = 'Max (W/C-ratio) %'
        min_max_form.materials_min_max_entries.entries[-1].max.data = 60

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
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        entry = cls._create_min_max_form_entry_internal(
            entries, uuids, name, material_type,
            ['Powder', 'Liquid'], 'Powder'
        )
        cls._populate_min_max_entry_with_default_values(entry, material_type)

    @classmethod
    def _populate_min_max_entry_with_default_values(cls, entry, type):
        if type == 'Admixture':
            entry.increment.label.text = 'Increment (Admixture/Powder-ratio) %'
            entry.increment.data = 1
            entry.min.label.text = 'Min (Admixture/Powder-ratio) %'
            entry.min.data = 2
            entry.max.label.text = 'Max (Admixture/Powder-ratio) %'
            entry.max.data = 4
        if type == 'Aggregates':
            entry.increment.data = 10
            entry.min.data = 50
            entry.max.data = 100
        if type == 'Custom':
            entry.increment.data = 5
            entry.min.data = 0
            entry.max.data = 20

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
                    ),
                    liquid=MaterialContent(
                        material=MaterialsFacade.get_material("liquid", combination["Liquid"]),
                        mass=combination_dict["Liquid"],
                    ) if "Liquid" in types else None,
                    admixture=MaterialContent(
                        material=MaterialsFacade.get_material("admixture", combination["Admixture"]),
                        mass=combination_dict["Admixture"],
                    ) if "Admixture" in types else None,
                    custom=MaterialContent(
                        material=MaterialsFacade.get_material("custom", combination["Custom"]),
                        mass=combination_dict["Custom"],
                    ) if "Custom" in types else None,
                    process=MaterialsFacade.get_process(combination_dict["Process"]) if "Process" in types else None,
                    aggregate=MaterialContent(
                        material=MaterialsFacade.get_material("aggregates", combination["Aggregates"]),
                    ) if "Aggregates" in types else None,
                    air_pore_content=None,
                )
            )

        return compositions

    @classmethod
    def _complete_composition(cls, c: Formulation, specific_gravities, constraint,
                              constraint_type: Literal["Volume", "Weight"]):
        # Equation for calculating dependent (powder) from absolute custom, relative liquid/admixture:
        # liquid * powder + aggregates + admixture * powder + custom + powder = constraint
        # powder * (liquid + admixture + 1) + aggregates + custom = constraint
        # powder = constraint - custom - aggregates / (liquid + admixture + 1)

        if constraint_type == "Volume":
            raise ValueError("Constraint type can not be 'Volume' for binders")

        c.total_mass = 0

        if c.custom:
            c.total_mass += c.custom.mass

        if c.aggregate:
            c.total_mass += c.aggregate.mass

        if c.powder:
            # Total mass contains (custom mass + aggregates mass) at this point
            c.powder.mass = (constraint - c.total_mass) / (
                (c.liquid.mass / 100 if c.liquid else 0)
                + (c.admixture.mass / 100 if c.admixture else 0)
                + 1
            )
            c.powder.mass = round(c.powder.mass, 2)
            c.total_mass += c.powder.mass

        # If we can't fit into the constraint, powder mass is negative -> invalid
        if c.powder.mass < 0:
            return None

        # Now we convert liquid and admixture masses from % of powder to actual kg
        if c.liquid:
            c.liquid.mass = round(c.liquid.mass * c.powder.mass / 100, 2)
            c.total_mass += c.liquid.mass

        if c.admixture:
            c.admixture.mass = round(c.admixture.mass * c.powder.mass / 100, 2)
            c.total_mass += c.admixture.mass

        return c

    @classmethod
    def _create_dataframe(cls, formulations):
        return cls._create_dataframe_internal(formulations, TEMPORARY_BINDER_FORMULATION)
