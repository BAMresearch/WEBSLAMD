import itertools
from typing import Literal

import pandas as pd

from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.constants import G_CM3_TO_KG_M3_CONVERSION_FACTOR
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.formulations.processing.models import ConcreteComposition, MaterialContent
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.concrete_selection_form import ConcreteSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.weight_input_preprocessor import WeightInputPreprocessor
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
    def create_formulation_batch(cls, formulations_data):
        return cls._create_formulation_batch_internal(formulations_data, TEMPORARY_CONCRETE_FORMULATION)

    @classmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, material_type):
        cls._create_min_max_form_entry_internal(entries, uuids, name, material_type, ['Powder', 'Liquid', 'Aggregates'],
                                                ['Aggregates', 'Air Pore Content'])

    @classmethod
    def _compute_weights_product(cls, all_materials_weights, constraint):
        return WeightsCalculator.compute_full_concrete_weights_product(all_materials_weights, constraint)

    @classmethod
    def _sort_materials(cls, materials_for_formulation):
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)

    @classmethod
    def _extract_material_uuids(cls, min_max_data):
        result = {}
        for item in min_max_data:
            material_type = item['type']
            uuids = item['uuid'].split(',')  # Split in case there are multiple UUIDs

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
    def _create_preliminary_compositions(cls, combination, param_space):
        types = list(param_space.keys())

        compositions = []
        for composition in itertools.product(*[param_space[mt] for mt in types]):
            combination_dict = dict(zip(types, composition))

            compositions.append(
                ConcreteComposition(
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
                    process=MaterialsFacade.get_process(combination_dict["Process"]) if "Process" else None,
                    aggregate=MaterialContent(
                        material=MaterialsFacade.get_material("aggregates", combination["Aggregates"]),
                    ),
                )
            )

        return compositions

    @classmethod
    def _complete_composition(cls, composition, specific_gravities, constraint, constraint_type: Literal["Volume", "Weight"]):
        c = composition
        total_volume = constraint * c.air_pore_content / 100 if c.air_pore_content is not None else 0
        total_mass = 0
        c.costs = 0
        c.co2_footprint = 0
        c.delivery_time = 0

        if c.powder:
            c.powder.volume = c.powder.mass / (specific_gravities[str(c.powder.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.powder.volume
            total_mass += c.powder.mass
            c.costs += c.powder.material.costs.costs or 0
            c.co2_footprint += c.powder.material.costs.co2_footprint or 0
            c.delivery_time += c.powder.material.costs.delivery_time or 0

        if c.liquid:
            c.liquid.volume = c.liquid.mass / (specific_gravities[str(c.liquid.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.liquid.volume
            total_mass += c.liquid.mass
            c.costs += c.liquid.material.costs.costs or 0
            c.co2_footprint += c.liquid.material.costs.co2_footprint or 0
            c.delivery_time += c.liquid.material.costs.delivery_time or 0

        if c.admixture:
            c.admixture.volume = c.admixture.mass / (
                    specific_gravities[str(c.admixture.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.admixture.volume
            total_mass += c.admixture.mass
            c.costs += c.admixture.material.costs.costs or 0
            c.co2_footprint += c.admixture.material.costs.co2_footprint or 0
            c.delivery_time += c.admixture.material.costs.delivery_time or 0

        if c.custom:
            c.custom.volume = c.custom.mass / (specific_gravities[str(c.custom.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.custom.volume
            total_mass += c.custom.mass
            c.costs += c.custom.material.costs.costs or 0
            c.co2_footprint += c.custom.material.costs.co2_footprint or 0
            c.delivery_time += c.custom.material.costs.delivery_time or 0

        if c.process:
            c.costs += c.process.costs.costs or 0
            c.co2_footprint += c.process.costs.co2_footprint or 0
            c.delivery_time += c.process.costs.delivery_time or 0

        if constraint_type == "Volume" and total_volume > constraint:
            return None
        elif constraint_type == "Weight" and total_mass > constraint:
            return None

        if constraint_type == "Volume":
            c.aggregate.volume = constraint - total_volume
            c.aggregate.mass = round(
                c.aggregate.volume * specific_gravities[str(c.aggregate.material.uuid)] * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2
            )
        elif constraint_type == "Weight":
            c.aggregate.mass = round(constraint - total_mass, 2)
        else:
            raise ValueError("Invalid constraint type: " + str(constraint_type))

        # TODO Weighted costs
        c.costs += c.aggregate.material.costs.costs or 0
        c.co2_footprint += c.aggregate.material.costs.co2_footprint or 0
        c.delivery_time += c.aggregate.material.costs.delivery_time or 0

        return c

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
    def _create_dataframe(cls, compositions):
        rows = []
        for idx, comp in enumerate(compositions):
            row = {
                'Idx_Sample': idx,
                'Powder (kg)': comp.powder.mass,
                'Liquid (kg)': comp.liquid.mass,
                'Aggregates (kg)': comp.aggregate.mass,
                'Materials': ", ".join(filter(None, [
                    comp.powder.material.name if comp.powder else None,
                    comp.liquid.material.name if comp.liquid else None,
                    comp.admixture.material.name if comp.admixture else None,
                    comp.custom.material.name if comp.custom else None,
                    comp.aggregate.material.name if comp.aggregate else None,
                    comp.process.name if comp.process else None,
                ])),
                'total costs': comp.costs,
                'total co2_footprint': comp.co2_footprint,
                'total delivery_time': comp.delivery_time,
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        return df

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
            if completed_composition := cls._complete_composition(composition, specific_gravities, constraint, constraint_type):
                completed_compositions.append(completed_composition)

        # TODO: Fix binders
        # TODO: Warning popup in frontend
        # TODO: Processes
        return cls._create_dataframe(completed_compositions)
