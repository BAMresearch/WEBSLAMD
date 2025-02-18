import itertools

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.formulations.processing.models import ConcreteComposition, Material
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.concrete_selection_form import ConcreteSelectionForm
from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.volumes_calculator import VolumesCalculator, G_CM3_TO_KG_M3_CONVERSION_FACTOR
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
    def _find_material_combinations(cls, type_to_uuids):
        material_types = list(type_to_uuids.keys())
        uuid_lists = [type_to_uuids[material_type] for material_type in material_types]

        raw_combinations = itertools.product(*uuid_lists)

        combinations = []
        for combination in raw_combinations:
            combination_dict = {material_type: uuid for material_type, uuid in zip(material_types, combination)}
            combinations.append(combination_dict)

        return combinations

    @classmethod
    def _create_preliminary_compositions(cls, material_combination, material_space):
        material_types = list(material_space.keys())

        compositions = []
        for combination in itertools.product(*[material_space[mt] for mt in material_types]):
            combination_dict = dict(zip(material_types, combination))
            compositions.append(
                ConcreteComposition(
                    powder=Material(uuid=material_combination["Powder"],
                                    mass=combination_dict["Powder"],
                                    volume=None) if "Powder" in material_types else None,
                    liquid=Material(uuid=material_combination["Liquid"],
                                    mass=combination_dict["Liquid"] * combination_dict["Powder"] / 100,
                                    volume=None) if "Liquid" in material_types else None,
                    admixture=Material(uuid=material_combination["Admixture"],
                                       mass=combination_dict["Admixture"] * combination_dict["Powder"] / 100,
                                       volume=None) if "Admixture" in material_types else None,
                    custom=Material(uuid=material_combination["Custom"],
                                    mass=combination_dict["Custom"],
                                    volume=None) if "Custom" in material_types else None,
                    air_pore_content=combination_dict["Air Pore Content"],
                    aggregate=Material(uuid=material_combination["Aggregates"], mass=None, volume=None),
                )
            )

        return compositions

    @classmethod
    def _complete_composition(cls, composition, specific_gravities, volume_constraint):
        c = composition
        total_volume = volume_constraint * c.air_pore_content / 100

        if c.powder:
            c.powder.volume = c.powder.mass / (specific_gravities[c.powder.uuid] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.powder.volume

        if c.liquid:
            c.liquid.volume = c.liquid.mass / (specific_gravities[c.liquid.uuid] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.liquid.volume

        if c.admixture:
            c.admixture.volume = c.admixture.mass / (
                    specific_gravities[c.admixture.uuid] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.admixture.volume

        if c.custom:
            c.custom.volume = c.custom.mass / (specific_gravities[c.custom.uuid] * G_CM3_TO_KG_M3_CONVERSION_FACTOR)
            total_volume += c.custom.volume

        if total_volume > volume_constraint:
            return None

        c.aggregate.volume = volume_constraint - total_volume
        c.aggregate.mass = round(
            c.aggregate.volume * specific_gravities[c.aggregate.uuid] * G_CM3_TO_KG_M3_CONVERSION_FACTOR, 2
        )

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
    def generate_formulations_with_weights_for_volume_constraint(cls, min_max_data, volume_constraint):
        weights_and_ratios = WeightInputPreprocessor.collect_weights_as_dict(min_max_data)
        materials = cls._extract_material_uuids(min_max_data)
        specific_gravities = cls._get_specific_gravities(materials)
        material_combinations = cls._find_material_combinations(materials)

        compositions = []
        for material_combination in material_combinations:
            compositions.extend(
                cls._create_preliminary_compositions(material_combination, weights_and_ratios))

        completed_compositions = []
        for composition in compositions:
            if completed_composition := cls._complete_composition(composition, specific_gravities, volume_constraint):
                completed_compositions.append(completed_composition)

        # TODO: Create dataframe
        # TODO: Apply logic to weight based constraints
        # TODO: Fix binders
        return

        #
        # material_combinations = cls._generate_material_combinations(material_volumes)
        #
        # material_volumes_for_all_combinations = VolumesCalculator.generate_volumes_for_combinations(material_combinations)
        #
        # valid_volumes_for_all_combinations = VolumesCalculator.validate_volume_combinations(material_volumes_for_all_combinations, min_max_data["constraint"])
        #
        # valid_formulations_with_aggregates = VolumesCalculator.add_aggregates_volume_to_combination(valid_volumes_for_all_combinations, specific_gravities, min_max_data["constraint"])
        #
        # formulations_with_weights = VolumesCalculator.transform_volumes_to_weights(valid_formulations_with_aggregates, specific_gravities, admixture_and_custom_materials_indices)
        #
        # return formulations_with_weights

    @classmethod
    def generate_formulations_with_weights_for_weight_constraint(cls, min_max_data, weight_constraint):
        materials_weights_and_ratios = WeightInputPreprocessor.collect_weights(min_max_data)
        materials_in_formulation = [material.get('type') for material in min_max_data]

        admixture_and_custom_materials_indices = cls._calculate_admixture_and_custom_indices(materials_in_formulation)
        material_weights = WeightsCalculator.compute_weights_from_ratios(
            materials_weights_and_ratios,
            admixture_and_custom_materials_indices
        )
        weights_combinations = list(product(*material_weights))
        formulations_with_aggregates = WeightsCalculator.add_aggregates_weight_to_weight_combinations(
            weights_combinations, float(weight_constraint)
        )

        return formulations_with_aggregates
