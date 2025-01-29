import os
from uuid import UUID

from slamd.common.session_backup.session_service import SessionService
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.design_assistant_service import DesignAssistantService
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.aggregates import Composition as AggregatesComposition
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Composition as LiquidComposition
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder, Structure
from slamd.materials.processing.models.process import Process


def _mock_find_all_materials():
    return [[Powder(uuid=UUID('5afe6e21-4f11-11ed-8732-a05950ec4f04'), type=str(MaterialType.POWDER.value),
                    structure=Structure(fine=5))],
            [Liquid(uuid=UUID('69162ae6-4f11-11ed-b9a6-a05950ec4f04'), type=str(MaterialType.LIQUID.value),
                    composition=LiquidComposition(na2_o=3))],
            [Aggregates(uuid=UUID('86e70486-4f11-11ed-910e-a05950ec4f04'), type=str(MaterialType.AGGREGATES.value),
                        composition=AggregatesComposition())],
            [Admixture(uuid=UUID('8fee9a00-4f11-11ed-be28-a05950ec4f04'), type=str(MaterialType.ADMIXTURE.value))],
            [Custom(uuid=UUID('96dcb8ec-4f11-11ed-971c-a05950ec4f04'), type=str(MaterialType.CUSTOM.value))]]


def _mock_find_all_processes():
    return [Process(uuid=UUID('9bbd7cfa-4f11-11ed-9bcc-a05950ec4f04'), type='process')]


def _mock_find_all_datasets():
    # Use MockMaterial to also mock datasets - they have the same interface
    return []


def _mock_get_session_for_propery(input):
    return {"zero_shot_learner": {"type": "Concrete"}, "dataset": "None"}


def test_convert_session_to_json_string(monkeypatch):
    monkeypatch.setattr(MaterialsPersistence, 'find_all_materials', _mock_find_all_materials)
    monkeypatch.setattr(MaterialsPersistence, 'find_all_processes', _mock_find_all_processes)
    monkeypatch.setattr(DiscoveryPersistence, 'find_all_datasets', _mock_find_all_datasets)
    monkeypatch.setattr(DesignAssistantPersistence, 'get_session_for_property', _mock_get_session_for_propery)

    session_as_json = SessionService.convert_session_to_json_string()

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'common', 'session', 'test_session.json')
    path_to_test_session = os.path.abspath(file_path)

    with open(path_to_test_session) as f:
        # JSON file is assumed to only contain one long line. splitlines removes newline.
        assert session_as_json == f.readline().splitlines()[0]


def test_load_session_from_json_string(monkeypatch):
    saved_materials = {}
    saved_datasets = []
    da_session = {}

    def _mock_save_material(mat_type, mat):
        if mat_type not in saved_materials:
            saved_materials[mat_type] = [mat]
        else:
            saved_materials[mat_type].append(mat)

    def _mock_save_dataset(dataset):
        saved_datasets.append(dataset)

    def _mock_instantiate_da_session_on_upload(mock_da_session):
        da_session['design_assistant'] = mock_da_session

    monkeypatch.setattr(MaterialsPersistence, 'save', _mock_save_material)
    monkeypatch.setattr(DiscoveryPersistence, 'save_dataset', _mock_save_dataset)
    monkeypatch.setattr(DesignAssistantService, 'instantiate_da_session_on_upload',
                        _mock_instantiate_da_session_on_upload)

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'common', 'session', 'test_session.json')
    path_to_test_session = os.path.abspath(file_path)

    with open(path_to_test_session) as f:
        # JSON file is assumed to only contain one long line. splitlines removes newline.
        session_data_string = f.readline()

        SessionService.load_session_from_json_string(session_data_string)

    assert frozenset(saved_materials.keys()) == frozenset(['powder', 'process', 'aggregates', 'admixture', 'liquid',
                                                           'custom'])
    assert str(saved_materials['powder'][0].uuid) == '5afe6e21-4f11-11ed-8732-a05950ec4f04'
    assert str(saved_materials['liquid'][0].uuid) == '69162ae6-4f11-11ed-b9a6-a05950ec4f04'
    assert saved_materials['powder'][0].structure.fine == 5
    assert saved_materials['liquid'][0].composition.na2_o == 3
    assert da_session['design_assistant'] == {'dataset': 'None', 'zero_shot_learner': {'type': 'Concrete'}}