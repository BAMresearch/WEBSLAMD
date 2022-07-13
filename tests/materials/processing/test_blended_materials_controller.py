import json

from slamd.materials.processing.materials_persistence import MaterialsPersistence
from tests.materials.materials_test_data import create_test_powders, create_test_aggregates


def test_blended_materials_controller_shows_initial_blended_materials_form_and_table(client, monkeypatch):
    def mock_query_by_type(input):
        if input == 'powder':
            powders = create_test_powders()
            powders[0].is_blended = True
            return powders
        return []

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

    response = client.get('/materials/blended')

    assert response.status_code == 200

    html = response.data.decode('utf-8')
    assert 'Blended base materials' in html
    assert 'Name' in html
    assert 'Material type' in html
    assert 'test powder' in html
    assert '<option value="test uuid1">test powder</option>' not in html
    assert '<option value="test uuid2">my powder</option>' in html

    assert 'All blended materials' in html
    assert '<td>test powder</td>' in html
    assert '<td>my powder</td>' not in html


def test_blended_materials_controller_loads_correct_selection_after_choosing_type(client, monkeypatch):
    def mock_query_by_type(input):
        if input == 'aggregates':
            return create_test_aggregates()
        return []

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

    response = client.get('/materials/blended/aggregates')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'test aggregate' in template
    assert 'Blended base materials' not in template
    assert 'Material type' not in template


def test_blended_materials_controller_adds_min_max_form(client, monkeypatch):
    response = client.get('/materials/blended/add_min_max_entries/2')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'all_min_max_entries-0-blended_material_name' in template
    assert 'all_min_max_entries-0-increment' in template
    assert 'all_min_max_entries-0-min' in template
    assert 'all_min_max_entries-0-max' in template

    assert 'all_min_max_entries-1-blended_material_name' in template
    assert 'all_min_max_entries-1-increment' in template
    assert 'all_min_max_entries-1-min' in template
    assert 'all_min_max_entries-1-max' in template

    assert 'Blended base materials' not in template
    assert 'Material type' not in template
