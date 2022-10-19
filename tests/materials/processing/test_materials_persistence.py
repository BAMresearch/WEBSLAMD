from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.liquid import Liquid


def test_query_by_type_calls_session(monkeypatch):
    mock_get_session_property_called_with = None

    def mock_get_session_property(input):
        nonlocal mock_get_session_property_called_with
        mock_get_session_property_called_with = input
        return [{'name': 'test name'}]

    monkeypatch.setattr(MaterialsPersistence,
                        'get_session_property', mock_get_session_property)
    result = MaterialsPersistence.query_by_type('powder')

    assert result == [{'name': 'test name'}]
    assert mock_get_session_property_called_with == 'powder'


def test_saves_sets_new_material_for_type(monkeypatch):

    def mock_get_session_property(input):
        return []

    mock_set_session_property_called_with = None

    def mock_set_session_property(type, materials):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = type, materials
        return None

    monkeypatch.setattr(MaterialsPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(MaterialsPersistence,
                        'set_session_property', mock_set_session_property)

    powder = Powder()
    MaterialsPersistence.save('powder', powder)
    assert mock_set_session_property_called_with == ('powder', [powder])


def test_adds_material_to_existing_ones_of_same_type(monkeypatch):
    def mock_get_session_property(input):
        if input == 'powder':
            return [Powder(name='test name')]
        return []

    mock_extend_session_property_called_with = None

    def mock_extend_session_property(type, material):
        nonlocal mock_extend_session_property_called_with
        mock_extend_session_property_called_with = type, material
        return None

    monkeypatch.setattr(MaterialsPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(MaterialsPersistence,
                        'extend_session_property', mock_extend_session_property)

    powder = Powder()
    MaterialsPersistence.save('powder', powder)
    assert mock_extend_session_property_called_with == ('powder', powder)


# In real use cases a UUID object is used. For simplicity and sake of this test it can be a simple string.
def test_delete_by_type_and_uuid_removes_material_of_specified_type(monkeypatch):
    to_be_removed = Powder()
    to_be_removed.uuid = 'to be removed'

    to_be_kept = Powder()
    to_be_kept.uuid = 'to be kept'

    def mock_get_session_property(input):
        if input == 'powder':
            return [to_be_removed, to_be_kept]
        return []

    mock_set_session_property_called_with = None

    def mock_set_session_property(type, materials):
        nonlocal mock_set_session_property_called_with
        mock_set_session_property_called_with = type, materials
        return None

    monkeypatch.setattr(MaterialsPersistence,
                        'get_session_property', mock_get_session_property)
    monkeypatch.setattr(MaterialsPersistence,
                        'set_session_property', mock_set_session_property)

    MaterialsPersistence.delete_by_type_and_uuid('powder', 'to be removed')
    assert mock_set_session_property_called_with == ('powder', [to_be_kept])

# In real use cases a UUID object is used. For simplicity and sake of this test it can be a simple string.
def test_query_by_type_and_uuid(monkeypatch):
    to_be_returned = Powder()
    to_be_returned.uuid = 'to be returned'

    def mock_get_session_property(input):
        if input == 'powder':
            return [to_be_returned, Powder()]
        else:
            return [Liquid(), Liquid()]

    monkeypatch.setattr(MaterialsPersistence, 'get_session_property', mock_get_session_property)

    correct_type = MaterialsPersistence.query_by_type_and_uuid('powder', 'to be returned')
    assert correct_type == to_be_returned

    incorrect_type = MaterialsPersistence.query_by_type_and_uuid('liquid', 'to be returned')
    assert incorrect_type == None
