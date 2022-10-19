from slamd import create_app
from slamd.materials.processing.forms.admixture_form import AdmixtureForm
from slamd.materials.processing.forms.aggregates_form import AggregatesForm
from slamd.materials.processing.forms.liquid_form import LiquidForm
from slamd.materials.processing.forms.powder_form import PowderForm
from slamd.materials.processing.base_materials_service import BaseMaterialService
from slamd.materials.processing.forms.process_form import ProcessForm
from slamd.materials.processing.materials_service import MaterialsResponse


def test_slamd_shows_form_and_table(client, monkeypatch):
    def mock_list_materials(blended):
        return MaterialsResponse(
            [{'uuid': 'test', 'name': 'test powder', 'type': 'Powder'}],
            'base materials / processes'
        )

    monkeypatch.setattr(BaseMaterialService, 'list_materials', mock_list_materials)

    response = client.get('/materials/base')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Name' in html
    assert 'Material type' in html
    assert 'CO₂ footprint' in html
    assert 'Costs' in html
    assert 'Delivery time' in html

    assert 'All base materials / processes' in html
    assert 'test powder' in html
    assert 'Powder' in html


def test_slamd_selects_powder(client):
    response = client.get('/materials/base/powder')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Fe₂O₃' in template
    assert 'SiO₂' in template
    assert 'Al₂O₃' in template
    assert 'CaO' in template
    assert 'MgO' in template
    assert 'Na₂O' in template
    assert 'K₂O' in template
    assert 'SO₃' in template
    assert 'TiO₂' in template
    assert 'P₂O₅' in template
    assert 'SrO' in template
    assert 'Mn₂O₃' in template

    assert '4 - Composition' in template
    assert '5 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_liquid(client):
    response = client.get('/materials/base/liquid')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Na₂SiO₃ (m%)' in template
    assert 'Na₂SiO₃ (mol%)' in template
    assert 'NaOH (m%)' in template
    assert 'NaOH (mol%)' in template
    assert 'SiO₂ (m%)' in template
    assert 'SiO₂ (mol%)' in template
    assert 'Na₂O (m%)' in template
    assert 'Na₂O (mol%)' in template
    assert 'H₂O (m%)' in template
    assert 'H₂O (mol%)' in template

    assert '4 - Composition' in template
    assert '5 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_aggregates(client):
    response = client.get('/materials/base/aggregates')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Fine Aggregates' in template
    assert 'Coarse Aggregates' in template
    assert 'Specific gravity' in template
    assert 'Bulk density' in template
    assert 'Fineness modulus' in template
    assert 'Water absorption' in template

    assert '4 - Composition' in template
    assert '5 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_admixture(client):
    response = client.get('/materials/base/admixture')
    template = response.json['template']

    assert response.status_code == 200

    assert '4 - Composition' not in template
    assert '4 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_custom(client):
    response = client.get('/materials/base/custom')
    template = response.json['template']

    assert response.status_code == 200

    assert '4 - Composition' not in template
    assert '4 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_process(client):
    response = client.get('/materials/base/process')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Duration' in template
    assert 'Temperature' in template
    assert 'Relative Humidity' in template

    assert '5 - Additional Properties - Leave empty if not needed.' in template


def test_slamd_selects_invalid_type_and_shows_error_page(client):
    response = client.get('/materials/base/invalid')

    html = response.data.decode('utf-8')
    assert response.status_code == 404

    assert 'Resource not found: The requested type' in html


def test_slamd_creates_new_powder_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_material(submitted_material):
        return (True, None)

    with app.test_request_context('/materials'):
        monkeypatch.setattr(BaseMaterialService, 'save_material', mock_save_material)
        form = PowderForm(material_name='test powder', material_type='Powder')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test powder' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_liquid_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_material(submitted_material):
        return (True, None)

    with app.test_request_context('/materials/base'):
        monkeypatch.setattr(BaseMaterialService, 'save_material', mock_save_material)
        form = LiquidForm(material_name='test liquid', material_type='Liquid')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test liquid' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_aggregates_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_material(submitted_material):
        return (True, None)

    with app.test_request_context('/materials/base'):
        monkeypatch.setattr(BaseMaterialService, 'save_material', mock_save_material)
        form = AggregatesForm(material_name='test aggregates', material_type='Aggregates')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test aggregates' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_process_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_material(submitted_material):
        return (True, None)

    with app.test_request_context('/materials/base'):
        monkeypatch.setattr(BaseMaterialService, 'save_material', mock_save_material)
        form = ProcessForm(material_name='test process', material_type='Process')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test process' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_admixture_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_material(submitted_material):
        return (True, None)

    with app.test_request_context('/materials/base'):
        monkeypatch.setattr(BaseMaterialService, 'save_material', mock_save_material)
        form = AdmixtureForm(material_name='test admixture', material_type='admixture')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test admixture' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_deletes_powder_and_returns_new_table_but_does_not_rerender_complete_page(client, monkeypatch):
    def mock_delete_material(type, uuid):
        return [{'uuid': 'test', 'name': 'test powder'}]

    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    response = client.delete('/materials/base/powder/123')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Actions' in template
    assert 'Name' in template
    assert 'Type' in template
    assert 'Properties' in template

    # Some sample fields which are part of the form but not returned by the delete
    # request as only the table is updated after deleting
    assert 'Material type' not in template
    assert 'CO2-Footprint' not in template
    assert 'Costs' not in template
