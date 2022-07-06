from slamd.materials.materials_persistence import MaterialsPersistence
from slamd.materials.model.powder import Powder


def test_query_by_type_calls_session(monkeypatch):
    mock_get_session_property_called_with = None

    def mock_get_session_property(input):
        nonlocal mock_get_session_property_called_with
        mock_get_session_property_called_with = input
        return [{'uuid': 'test uuid', 'name': 'test name'}]

    monkeypatch.setattr(MaterialsPersistence, 'get_session_property', mock_get_session_property)
    result = MaterialsPersistence.query_by_type('powder')

    assert result == [{'uuid': 'test uuid', 'name': 'test name'}]
    assert mock_get_session_property_called_with == 'powder'


def test_saves_sets_new_material_for_type(monkeypatch):

    def mock_get_session_property(input):
        return []

    mock_set_session_property_called_with = None

    def mock_set_session_property(type, material):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = type, material
        return None

    monkeypatch.setattr(MaterialsPersistence, 'get_session_property', mock_get_session_property)
    monkeypatch.setattr(MaterialsPersistence, 'set_session_property', mock_set_session_property)

    powder = Powder()
    MaterialsPersistence.save('powder', powder)
    assert mock_set_session_property_called_with == ('powder', [powder])


def test_adds_material_to_existing_ones_of_same_type(monkeypatch):

    def mock_get_session_property(input):
        if input == 'powder':
            return [{'uuid': 'test uuid', 'name': 'test_name'}]
        return []

    mock_extend_session_property_called_with = None

    def mock_extend_session_property(type, material):
        nonlocal mock_extend_session_property_called_with
        mock_extend_session_property_called_with = type, material
        return None

    monkeypatch.setattr(MaterialsPersistence, 'get_session_property', mock_get_session_property)
    monkeypatch.setattr(MaterialsPersistence, 'extend_session_property', mock_extend_session_property)

    powder = Powder()
    MaterialsPersistence.save('powder', powder)
    assert mock_extend_session_property_called_with == ('powder', powder)
