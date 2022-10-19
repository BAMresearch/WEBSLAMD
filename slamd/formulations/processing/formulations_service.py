from datetime import datetime

from werkzeug.utils import secure_filename

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION, \
    TEMPORARY_BINDER_FORMULATION
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.building_materials_factory import BuildingMaterialsFactory


class FormulationsService:

    @classmethod
    def load_formulations_page(cls, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        form = strategy.populate_selection_form()
        df = strategy.get_formulations()
        return form, df

    @classmethod
    def create_formulations_min_max_form(cls, formulation_selection, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.create_min_max_form(formulation_selection)

    @classmethod
    def create_weights_form(cls, weights_request_data, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.populate_weights_form(weights_request_data)

    @classmethod
    def create_materials_formulations(cls, formulations_data, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.create_formulation_batch(formulations_data)

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
    def delete_formulation(cls, building_material):
        if building_material == BuildingMaterial.BINDER.value:
            DiscoveryFacade.delete_dataset_by_name(TEMPORARY_BINDER_FORMULATION)
        elif building_material == BuildingMaterial.CONCRETE.value:
            DiscoveryFacade.delete_dataset_by_name(TEMPORARY_CONCRETE_FORMULATION)
        else:
            raise ValueNotSupportedException(message=f'Can not delete formulation. Invalid building_material: '
                                                     f'{building_material}')

    @classmethod
    def save_dataset(cls, form, building_material):
        filename = cls._sanitize_filename(form['dataset_name'])

        if building_material == BuildingMaterial.BINDER.value:
            temporary_filename = TEMPORARY_BINDER_FORMULATION
        elif building_material == BuildingMaterial.CONCRETE.value:
            temporary_filename = TEMPORARY_CONCRETE_FORMULATION
        else:
            raise ValueNotSupportedException(message=f'Could not save dataset. Invalid building_material: '
                                                     f'{building_material}')

        formulation_to_be_saved_as_dataset = DiscoveryFacade.query_dataset_by_name(temporary_filename)
        DiscoveryFacade.delete_dataset_by_name(temporary_filename)
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
            raise ValueNotSupportedException('The name of the file cannot start with "temporary"!')
        return filename
