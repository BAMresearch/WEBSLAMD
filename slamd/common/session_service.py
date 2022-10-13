import json

from flask import session

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


class SessionService:
    JSON_MAT_PROC_KEY = 'Materials_and_Processes'
    JSON_DATA_KEY = 'Datasets'

    @classmethod
    def save_session(cls):
        all_materials = MaterialsPersistence.find_all_materials()
        all_processes = MaterialsPersistence.find_all_processes()
        all_datasets = DiscoveryPersistence.find_all_datasets()

        full_json = {
            cls.JSON_MAT_PROC_KEY: [],
            cls.JSON_DATA_KEY: []
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
    def load_session(cls, session_data_json):
        session_data = json.loads(session_data_json)

        loaded_materials = [] # Collect all first in case of issues
        loaded_datasets = []

        # TODO add comment - no facade
        for dictionary in session_data[cls.JSON_MAT_PROC_KEY]:
            material_type = dictionary['type'].lower()
            if material_type == MaterialType.POWDER.value:
                material = Powder()
            elif material_type == MaterialType.LIQUID.value:
                material = Liquid()
            elif material_type == MaterialType.AGGREGATES.value:
                material = Aggregates()
            elif material_type == MaterialType.PROCESS.value:
                material = Process()
            elif material_type == MaterialType.ADMIXTURE.value:
                material = Admixture()
            elif material_type == MaterialType.CUSTOM.value:
                material = Custom()
            else:
                raise MaterialNotFoundException('The requested type is not supported!')

            material.from_dict(dictionary)
            loaded_materials.append((material_type, material))

        for dictionary in session_data[cls.JSON_DATA_KEY]:
            dataset = Dataset()
            dataset.from_dict(dictionary)
            loaded_datasets.append(dataset)

        for mat_type, mat in loaded_materials:
            MaterialsPersistence.save(mat_type, mat)

        for dataset in loaded_datasets:
            DiscoveryPersistence.save_dataset(dataset)




# Things to save: All base materials (Powders, Liquids, ...)
# All blended materials
# All datasets (formulations temp data set included)
# TSNE plot data? predictions? CSRF token?
# dataclass -> to dict function?