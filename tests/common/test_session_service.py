from dataclasses import dataclass

from slamd.common.session_service import SessionService
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.process import Process


@dataclass
class MockMaterial:
    type: str = 'powder'
    prop1: float = None
    prop2: str = None

    def to_dict(self):
        return {
            'type': self.type,
            'prop1': self.prop1,
            'prop2': self.prop2
        }

    @classmethod
    def from_dict(cls, dictionary):
        out = cls(**dictionary)
        return out


def _mock_find_all_materials():
    return [2 * [MockMaterial('powder', 1.1 * i, f'val{i}') for i in range(3)]]


def _mock_find_all_processes():
    return [MockMaterial('process', 1.1 * i, f'val{i}') for i in range(2)]


def _mock_find_all_datasets():
    # Use MockMaterial to also mock datasets - they have the same interface
    return [MockMaterial('not-a-material', 1.1 * i, f'val{i}') for i in range(2)]


def test_convert_session_to_json_string(monkeypatch):
    monkeypatch.setattr(MaterialsPersistence, 'find_all_materials', _mock_find_all_materials)
    monkeypatch.setattr(MaterialsPersistence, 'find_all_processes', _mock_find_all_processes)
    monkeypatch.setattr(DiscoveryPersistence, 'find_all_datasets', _mock_find_all_processes)

    session_as_json = SessionService.convert_session_to_json_string()

    with open('tests/common/session/test_session.json') as f:
        # JSON file is assumed to only contain one long line. splitlines removes newline.
        assert session_as_json == f.readline().splitlines()[0]


def test_load_session_from_json_string(monkeypatch):
    saved_materials = {}
    saved_datasets = []

    def _mock_save_material(mat_type, mat):
        if mat_type not in saved_materials:
            saved_materials[mat_type] = [mat]
        else:
            saved_materials[mat_type].append(mat)

    def _mock_save_dataset(dataset):
        saved_datasets.append(dataset)

    def _mock_material_from_dict(dictionary):
        return MockMaterial.from_dict(dictionary)

    monkeypatch.setattr(MaterialsPersistence, 'save', _mock_save_material)
    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', _mock_save_dataset)
    monkeypatch.setattr(Powder, 'from_dict', _mock_material_from_dict)
    monkeypatch.setattr(Process, 'from_dict', _mock_material_from_dict)
    monkeypatch.setattr(Dataset, 'from_dict', _mock_material_from_dict)

    with open('tests/common/session/test_session.json') as f:
        # JSON file is assumed to only contain one long line. splitlines removes newline.
        session_data_string = f.readline()

        SessionService.load_session_from_json_string(session_data_string)

    assert list(saved_materials.keys()) == ['powder', 'process']
    assert len(saved_materials['powder']) == 6
    assert len(saved_materials['process']) == 2
