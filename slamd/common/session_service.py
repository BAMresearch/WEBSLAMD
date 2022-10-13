import json

from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.materials.processing.materials_persistence import MaterialsPersistence


class SessionService:

    @classmethod
    def save_session(cls):
        all_materials = MaterialsPersistence.find_all_materials()
        all_processes = MaterialsPersistence.find_all_processes()
        all_datasets = DiscoveryPersistence.find_all_datasets()

        full_json = {
            'Materials_and_Processes': [],
            'Datasets': []
        }

        for mat_list in all_materials:
            for mat in mat_list:
                full_json['Materials_and_Processes'].append(mat.to_dict())

        for proc in all_processes:
            full_json['Materials_and_Processes'].append(proc.to_dict())

        # for ds in all_datasets:
        #     full_json['Datasets'].append(ds.to_dict())
        #
        # full_string = json.dumps(full_json)
        # print(full_json)
        # print(full_string)
        #
        # reconstructed = json.loads(full_string)
        # print(reconstructed)


# Things to save: All base materials (Powders, Liquids, ...)
# All blended materials
# All datasets (formulations temp data set included)
# TSNE plot data? predictions? CSRF token?