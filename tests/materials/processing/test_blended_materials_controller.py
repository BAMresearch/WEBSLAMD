import json

from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy
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


def test_blended_materials_controller_adds_min_max_form_without_warning(client, monkeypatch):
    def mock_check_completeness_of_base_material_properties(input):
        return True

    monkeypatch.setattr(PowderStrategy, 'check_completeness_of_base_material_properties',
                        mock_check_completeness_of_base_material_properties)

    response = client.post('/materials/blended/add_min_max_entries/powder/2', data=b'[]')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']

    _assert_min_max_entries(template)

    assert 'The chosen configuration is not complete!' not in template

    assert 'Blended base materials' not in template
    assert 'Material type' not in template


def test_blended_materials_controller_adds_min_max_form_with_warning(client, monkeypatch):
    def mock_check_completeness_of_base_material_properties(input):
        return False

    monkeypatch.setattr(PowderStrategy, 'check_completeness_of_base_material_properties',
                        mock_check_completeness_of_base_material_properties)

    response = client.post('/materials/blended/add_min_max_entries/powder/2', data=b'[]')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    _assert_min_max_entries(template)

    assert 'The chosen configuration is not complete!' in template

    assert 'Blended base materials' not in template
    assert 'Material type' not in template


def _assert_min_max_entries(template):
    assert 'all_min_max_entries-0-blended_material_name' in template
    assert 'all_min_max_entries-0-increment' in template
    assert 'all_min_max_entries-0-min' in template
    assert 'all_min_max_entries-0-max' in template
    assert 'all_min_max_entries-1-blended_material_name' in template
    assert 'all_min_max_entries-1-increment' in template
    assert 'all_min_max_entries-1-min' in template
    assert 'all_min_max_entries-1-max' in template
