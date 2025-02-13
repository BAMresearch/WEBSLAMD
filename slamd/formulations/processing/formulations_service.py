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

        if formulations_data['selectedConstraintType'] == 'Volume':
            formulations_data = cls.compute_formulations_data_for_volume_constraint(strategy, formulations_data)
        else:
            # Implement formulations data for weight based
            pass
        # return strategy.create_formulation_batch(formulations_data)

        return formulations_data

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
    def get_specific_gravity_dict(cls, materials_dict):
        densities_dict = {}
        for material, uuids in materials_dict.items():
            material = material.lower()
            densities_dict[material] = []
            for uuid in uuids:
                session_value = MaterialsFacade.get_material_from_session(material, uuid)
                if session_value and hasattr(session_value, 'specific_gravity'):
                    densities_dict[material].append(session_value.specific_gravity)

        return densities_dict

    @classmethod
    def compute_formulations_data_for_volume_constraint(cls, strategy, request_data):
        formulation_materials_specific_gravities = (cls._get_specific_gravity_of_formulation_configuration(request_data
                                                                   ['materials_formulation_configuration']))
        formulations_with_weights = strategy.generate_formulations_with_weights_for_volume_constraint(request_data, formulation_materials_specific_gravities)

        formulations_data = cls._build_formulations_data(formulations_with_weights, request_data)
        return formulations_data

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
            formulation_data = {}
            formulation_data['materials_request_data'] = {'materials_formulation_configuration': formulation['materials']}
            formulation_data['weight_request_data'] = formulation['all_weights']
            formulation_data['processes_request_data'] = request_data['processesRequestData']
            formulation_data['samplingSize'] = request_data['samplingSize']
            formulations_data.append(formulation_data)

        return formulations_data
