from datetime import datetime
from itertools import product

from werkzeug.utils import secure_filename

from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException, \
    MaterialNotFoundException
from slamd.common.ml_utils import concat
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.building_materials_factory import BuildingMaterialsFactory
from slamd.formulations.processing.formulations_converter import FormulationsConverter
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations

MAX_DATASET_SIZE = 10000


class FormulationsService:

    @classmethod
    def load_formulations_page(cls, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        form, context = strategy.populate_selection_form()
        df = strategy.get_formulations()
        return form, df, context

    @classmethod
    def create_formulations_min_max_form(cls, formulation_selection, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.create_min_max_form(formulation_selection)

    @classmethod
    def create_weights_form(cls, weights_request_data, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.populate_weigths_form(weights_request_data)

    @classmethod
    def create_materials_formulations(cls, formulations_data):
        previous_batch_df = DiscoveryFacade.query_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)

        materials_data = formulations_data['materials_request_data']['materials_formulation_configuration']
        processes_data = formulations_data['processes_request_data']['processes']
        weights_data = formulations_data['weights_request_data']['all_weights']

        materials = cls._prepare_materials_for_taking_direct_product(materials_data)

        processes = []
        for process in processes_data:
            processes.append(MaterialsFacade.get_process(process['uuid']))

        if len(processes) > 0:
            materials.append(processes)

        combinations_for_formulations = list(product(*materials))

        dataframe = FormulationsConverter.formulation_to_df(combinations_for_formulations, weights_data)

        if previous_batch_df:
            dataframe = concat(previous_batch_df.dataframe, dataframe)

        if len(dataframe.index) > MAX_DATASET_SIZE:
            raise SlamdRequestTooLargeException(
                f'Formulation is too large. At most {MAX_DATASET_SIZE} rows can be created!')

        dataframe['Idx_Sample'] = range(0, len(dataframe))
        dataframe.insert(0, 'Idx_Sample', dataframe.pop('Idx_Sample'))

        temporary_dataset = Dataset(name=TEMPORARY_CONCRETE_FORMULATION, dataframe=dataframe)
        DiscoveryFacade.save_temporary_dataset(temporary_dataset, TEMPORARY_CONCRETE_FORMULATION)

        return dataframe

    @classmethod
    def _prepare_materials_for_taking_direct_product(cls, materials_data):
        powders = []
        liquids = []
        aggregates = []
        admixtures = []
        customs = []
        for materials_for_type_data in materials_data:
            uuids = materials_for_type_data['uuids'].split(',')
            for uuid in uuids:
                material_type = materials_for_type_data['type']
                if material_type.lower() == MaterialsFacade.POWDER:
                    powders.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.LIQUID:
                    liquids.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.AGGREGATES:
                    aggregates.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.ADMIXTURE:
                    admixtures.append(MaterialsFacade.get_material(material_type, uuid))
                elif material_type.lower() == MaterialsFacade.CUSTOM:
                    customs.append(MaterialsFacade.get_material(material_type, uuid))
                else:
                    raise MaterialNotFoundException('Cannot process the requested material!')

        # We sort the materials according to a) the fact that for concrete, aggregates is always the dependent material
        # in terms of the weight constraint thus appearing last and b) the order of appearance in the formulation UI
        materials_for_formulation = MaterialsForFormulations(powders, aggregates, liquids, admixtures, customs)
        return MaterialsFacade.sort_for_concrete_formulation(materials_for_formulation)

    @classmethod
    def _create_properties(cls, inner_dict):
        properties = ''
        for key, value in inner_dict.items():
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

    @classmethod
    def delete_formulation(cls):
        DiscoveryFacade.delete_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)

    @classmethod
    def save_dataset(cls, form):
        filename = cls._sanitize_filename(form['dataset_name'])
        formulation_to_be_saved_as_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)
        DiscoveryFacade.delete_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)
        formulation_to_be_saved_as_dataset.name = filename
        if formulation_to_be_saved_as_dataset:
            DiscoveryFacade.save_dataset(formulation_to_be_saved_as_dataset)

    @classmethod
    def _sanitize_filename(cls, user_input):
        if user_input == '':
            # Generate a filename to allow the user to create many datasets
            # one after the other, without having to enter a filename.
            user_input = f'Unnamed-Dataset-{datetime.now()}'

        if not user_input.endswith('.csv'):
            # Add the extension to make it clear which format the app supports
            # for downloading datasets. This may change in the future.
            user_input = user_input + '.csv'

        filename = secure_filename(user_input)
        if filename.startswith('temporary'):
            raise ValueNotSupportedException('The name of the file cannot start with temporary!')
        return filename
