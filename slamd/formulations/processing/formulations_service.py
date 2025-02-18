from datetime import datetime

from werkzeug.utils import secure_filename

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_CONCRETE_FORMULATION, \
    TEMPORARY_BINDER_FORMULATION
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.building_materials_factory import BuildingMaterialsFactory
from slamd.materials.processing.materials_facade import MaterialsFacade

class FormulationsService:

    @classmethod
    def load_formulations_page(cls, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        form = strategy.populate_selection_form()
        df = strategy.get_formulations()
        return form, df

    @classmethod
    def create_formulations_min_max_form(cls, formulation_selection, building_material, selected_constraint_type):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.create_min_max_form(formulation_selection, selected_constraint_type)

    @classmethod
    def create_weights_form(cls, weights_request_data, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)
        return strategy.populate_weights_form(weights_request_data)

    @classmethod
    def create_materials_formulations(cls, formulations_data, building_material):
        strategy = BuildingMaterialsFactory.create_building_material_strategy(building_material)

        if formulations_data['selected_constraint_type'] == 'Volume':
            formulations = strategy.generate_formulations_with_weights_for_volume_constraint(
                formulations_data["materials_request_data"]["min_max_data"],
                float(formulations_data["constraint"])
            )
            # formulations = cls._build_formulations_data(formulations_with_weights, formulations_data)
        else:
            formulations = cls._compute_formulations_data_for_weight_constraint(strategy, formulations_data)
            return strategy.create_formulation_batch(formulations)

        # return formulations

    @classmethod
    def _create_properties(cls, inner_dict):
        properties = ''
        for key, value in inner_dict.items():
            properties += f'{key}: {value}; '
        properties = properties.strip()[:-1]
        return properties

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

    @classmethod
    def _get_specific_gravity_of_formulation_configuration(cls, configuration):
        specific_gravities = []
        for material in configuration:
            material_type = material.get('type')
            material_uuids = material.get('uuid')
            if material_type in ['Powder', 'Liquid', 'Admixture', 'Aggregates', 'Custom']:
                material_uuids = material_uuids.split(',')
                for material_uuid in material_uuids:
                    material = MaterialsFacade.get_material_from_session(material_type, material_uuid)
                    specific_gravities.append({'uuid': material_uuid, 'type': material_type,'specific_gravity': material.specific_gravity})

        return specific_gravities

    @classmethod
    def _build_formulations_data(cls, formulations_with_weights, request_data):
        formulations_data = []
        for formulation in formulations_with_weights:
            for material in formulation['materials']:
                material['uuids'] = material.pop('uuid')
            formulation_data = {}
            formulation_data['materials_request_data'] = {'materials_formulation_configuration': formulation['materials']}
            formulation_data['weights_request_data'] = {'all_weights': formulation['all_weights']}
            formulation_data['processes_request_data'] = request_data['processesRequestData']
            formulation_data['sampling_size'] = request_data['samplingSize']
            formulations_data.append(formulation_data)

        return formulations_data

    @classmethod
    def _compute_formulations_data_for_weight_constraint(cls, strategy, request_data):
        formulations_data = {}
        formulations_data['all_weights'] = strategy.generate_formulations_with_weights_for_weight_constraint(
            request_data['materials_request_data']["min_max_data"], request_data["constraint"]
        )

        formulations_data['materials'] = request_data['materials_request_data']["min_max_data"]
        for material in formulations_data['materials']:
            material.pop('min')
            material.pop('max')
            material.pop('increment')

        formulations_data["processes_request_data"] = request_data["processes_request_data"]
        formulations_data["sampling_size"] = request_data["sampling_size"]

        return formulations_data
