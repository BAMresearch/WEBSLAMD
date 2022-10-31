from slamd import create_app
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from tests.materials.materials_test_data import create_test_powders, create_test_aggregates


def test_all_saved_base_materials_are_sorted_correctly_and_returned(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_query_by_type(input):
        if input == 'powder':
            return create_test_powders()
        elif input == 'aggregates':
            return create_test_aggregates()
        return []

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

    with app.test_request_context('/materials/base'):
        response = client.get('/materials/base')

    assert response.status_code == 200

    html = response.data.decode('utf-8')
    assert 'Costs (€/ton)' in html
    assert 'Fe₂O₃ (m%)' in html
    assert 'SiO₂ (m%)' in html
    assert 'Mn₂O₃ (m%)' in html
    assert 'LOI (m%)' in html
    assert 'Specific gravity (m%)' in html
    assert 'Add property' in html
    assert 'Delete last property' in html

    assert 'All base materials' in html
    assert 'Actions' in html
    assert 'Type' in html
    assert 'Name' in html
    assert 'Properties' in html

    assert 'my powder' in html
    assert 'test powder' in html
    assert 'Fe₂O₃ (m%): 23.3, Specific gravity (m%): 12, test prop: test value' in html
    assert 'test aggregate' in html
    assert 'Fine Aggregates (m%): 12, aggregate property: aggregate property value' in html
