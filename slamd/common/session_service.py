import json

from slamd.common.error_handling import MaterialNotFoundException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.process import Process

JSON_MAT_PROC_KEY = 'Materials_and_Processes'
JSON_DATA_KEY = 'Datasets'


class SessionService:

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
            for mat in mat_list:
                full_json['Materials_and_Processes'].append(mat.to_dict())

        for proc in all_processes:
            full_json['Materials_and_Processes'].append(proc.to_dict())

        for ds in all_datasets:
            full_json['Datasets'].append(ds.to_dict())

        full_string = json.dumps(full_json)
        return full_string

    @classmethod
    def load_session_from_json_string(cls, session_data_string):
        session_data = json.loads(session_data_string)

        # Collect all data first, then write into session, in case there is a problem while loading
        loaded_materials = []
        loaded_datasets = []

        # We decided to work with Material objects directly rather than building a facade for the material module:
        # "common" part of the code has knowledge about other parts; there is less overhead this way; the interaction
        # between this and materials is not part of the domain logic
        for dictionary in session_data[JSON_MAT_PROC_KEY]:
            material_type = dictionary['type'].lower()

            if material_type == MaterialType.POWDER.value:
                material = Powder()
            elif material_type == MaterialType.LIQUID.value:
                material = Liquid()
            elif material_type == MaterialType.AGGREGATES.value:
                material = Aggregates()
            elif material_type == MaterialType.PROCESS.value:
                # Processes are handled like every other material (including in MaterialPersistence)
                material = Process()
            elif material_type == MaterialType.ADMIXTURE.value:
                material = Admixture()
            elif material_type == MaterialType.CUSTOM.value:
                material = Custom()
            else:
                raise MaterialNotFoundException(f'The requested type {material_type} is not supported!')

            material.from_dict(dictionary)
            loaded_materials.append((material_type, material))

        for dictionary in session_data[JSON_DATA_KEY]:
            dataset = Dataset()
            dataset.from_dict(dictionary)
            loaded_datasets.append(dataset)

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

