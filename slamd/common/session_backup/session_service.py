import json
from datetime import datetime

import pandas as pd

from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy

JSON_MAT_PROC_KEY = 'Materials_and_Processes'
JSON_DATA_KEY = 'Datasets'


class SessionService:

    @classmethod
    def create_default_filename(cls):
        return datetime.now().strftime('session_%Y-%m-%d_%H%M%S.json')

    @classmethod
    def convert_session_to_json_string(cls):
        all_materials = MaterialsPersistence.find_all_materials()
        all_processes = MaterialsPersistence.find_all_processes()
        all_datasets = DiscoveryPersistence.find_all_datasets()

        full_json = {
            JSON_MAT_PROC_KEY: [],
            JSON_DATA_KEY: []
        }

        for mat_list in all_materials:
            if not mat_list:
                continue

            mat_strat = MaterialFactory.create_strategy(mat_list[0].type)
            for mat in mat_list:
                full_json['Materials_and_Processes'].append(mat_strat.convert_material_to_dict(mat))

        for proc in all_processes:
            full_json['Materials_and_Processes'].append(ProcessStrategy.convert_material_to_dict(proc))

        for ds in all_datasets:
            full_json['Datasets'].append(cls._convert_dataset_to_dict(ds))

        full_string = json.dumps(full_json)
        return full_string

    @classmethod
    def load_session_from_json_string(cls, session_data_string):
        try:
            session_data = json.loads(session_data_string)
        except ValueError:
            raise SlamdUnprocessableEntityException(message='Not a valid JSON file')

        # Collect all data first, then write into session, in case there is a problem while loading
        loaded_materials = []
        loaded_datasets = []

        # We decided to work with Material objects directly rather than building a facade for the material module:
        # "common" part of the code has knowledge about other parts; there is less overhead this way; the interaction
        # between this and materials is not part of the domain logic
        for dictionary in session_data[JSON_MAT_PROC_KEY]:
            material_type = dictionary['type'].lower()
            strategy = MaterialFactory.create_strategy(material_type)

            loaded_materials.append(
                (material_type, strategy.create_material_from_dict(dictionary))
            )

        for dictionary in session_data[JSON_DATA_KEY]:
            loaded_datasets.append(cls._create_dataset_from_dict(dictionary))

        for mat_type, mat in loaded_materials:
            MaterialsPersistence.save(mat_type, mat)

        for dataset in loaded_datasets:
            DiscoveryPersistence.save_dataset(dataset)

    @classmethod
    def clear_session(cls):
        all_materials = MaterialsPersistence.find_all_materials()
        all_processes = MaterialsPersistence.find_all_processes()
        all_datasets = DiscoveryPersistence.find_all_datasets()

        for mat_list in all_materials:
            for mat in mat_list:
                MaterialsPersistence.delete_by_type_and_uuid(mat.type, str(mat.uuid))

        for proc in all_processes:
            MaterialsPersistence.delete_by_type_and_uuid(proc.type, str(proc.uuid))

        for ds in all_datasets:
            DiscoveryPersistence.delete_dataset_by_name(ds.name)

    @classmethod
    def _convert_dataset_to_dict(cls, dataset):
        return {
            'name': dataset.name,
            'target_columns': dataset.target_columns,
            'dataframe': dataset.dataframe.to_dict()
        }

    @classmethod
    def _create_dataset_from_dict(cls, dictionary):
        dataset = Dataset(
            name=dictionary['name'],
            target_columns=dictionary['target_columns'],
        )
        dataset.dataframe = pd.DataFrame.from_dict(dictionary['dataframe'])
        dataset.dataframe = dataset.dataframe.reset_index(drop=True)

        return dataset


