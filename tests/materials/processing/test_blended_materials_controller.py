import json

from slamd import create_app
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from tests.materials.materials_test_data import create_test_powders, create_test_aggregates


def test_blended_materials_controller_shows_initial_blended_materials_form(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_query_by_type(input):
        if input == 'powder':
            return create_test_powders()
        return []

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

    with app.test_request_context('/materials/blended'):

        response = client.get('/materials/blended')

    assert response.status_code == 200

    html = response.data.decode('utf-8')
    assert 'Blended base materials' in html
    assert 'Name' in html
    assert 'Material type' in html
    assert 'test powder' in html
    assert 'my powder' in html


def test_blended_materials_controller_loads_correct_selection_after_choosing_type(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_query_by_type(input):
        if input == 'aggregates':
            return create_test_aggregates()
        return []

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

    with app.test_request_context('/materials/blended'):

        response = client.get('/materials/blended/aggregates')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'test aggregate' in template
    assert 'Blended base materials' not in template
    assert 'Name' not in template
    assert 'Material type' not in template
