from slamd import create_app
from slamd.materials.processing.forms.admixture_form import AdmixtureForm
from slamd.materials.processing.forms.aggregates_form import AggregatesForm
from slamd.materials.processing.forms.liquid_form import LiquidForm
from slamd.materials.processing.forms.powder_form import PowderForm
from slamd.materials.processing.base_materials_service import BaseMaterialService
from slamd.materials.processing.forms.process_form import ProcessForm
from slamd.materials.processing.materials_service import MaterialsResponse


def test_slamd_shows_form_and_table(client, mocker):
    mock_response = MaterialsResponse([{'uuid': 'test', 'name': 'test powder', 'type': 'Powder'}], 'base')
    mocker.patch.object(BaseMaterialService, 'list_materials',
                        autospec=True, return_value=mock_response)
    response = client.get('/materials/base')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Name' in html
    assert 'Material type' in html
    assert 'CO₂ footprint' in html
    assert 'Costs' in html
    assert 'Delivery time' in html

    assert 'All base materials' in html
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


def test_slamd_selects_liquid(client):
    response = client.get('/materials/base/liquid')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Na₂SiO₃' in template
    assert 'NaOH' in template
    assert 'Na₂SiO₃ specific' in template
    assert 'NaOH specific' in template
    assert 'Total solution' in template
    assert 'Na₂O (I)' in template
    assert 'SiO₂ (I)' in template
    assert 'H₂O' in template
    assert 'Na₂O (dry)' in template
    assert 'SiO₂ (dry)' in template
    assert 'Water' in template
    assert 'Total NaOH' in template


def test_slamd_selects_aggregates(client):
    response = client.get('/materials/base/aggregates')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Fine Aggregates' in template
    assert 'Coarse Aggregates' in template
    assert 'FA Density' in template
    assert 'CA Density' in template


def test_slamd_selects_admixture(client):
    response = client.get('/materials/base/admixture')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Composition' in template
    assert 'Type' in template


def test_slamd_selects_custom(client):
    response = client.get("/materials/base/custom")
    template = response.json['template']

    assert response.status_code == 200
    assert 'Name' in template
    assert 'Value' in template


def test_slamd_selects_process(client):
    response = client.get('/materials/base/process')
    template = response.json['template']

    assert response.status_code == 200
    assert 'Duration' in template
    assert 'Temperature' in template
    assert 'Relative Humidity' in template


def test_slamd_selects_invalid_type_and_shows_error_page(client):
    response = client.get('/materials/base/invalid')

    html = response.data.decode('utf-8')
    assert response.status_code == 404

    assert 'Resource not found: The requested type is not supported!' in html


def test_slamd_creates_new_powder_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        mocker.patch.object(BaseMaterialService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = PowderForm(material_name='test powder', material_type='Powder')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test powder' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_liquid_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials/base'):
        mocker.patch.object(BaseMaterialService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = LiquidForm(material_name='test liquid', material_type='Liquid')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test liquid' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_aggregates_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials/base'):
        mocker.patch.object(BaseMaterialService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = AggregatesForm(
            material_name='test aggregates', material_type='Aggregates')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test aggregates' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_process_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials/base'):
        mocker.patch.object(BaseMaterialService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = ProcessForm(
            material_name='test process', material_type='Process')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test process' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_creates_new_admixture_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials/base'):
        mocker.patch.object(BaseMaterialService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = AdmixtureForm(
            material_name='test admixture', material_type='admixture')

        response = client.post('/materials/base', data=form.data)

    assert response.status_code == 302
    assert b'test admixture' not in response.data
    assert response.request.path == '/materials/base'


def test_slamd_deletes_powder_and_returns_new_table_but_does_not_rerender_complete_page(client, mocker):
    mock_response = [{'uuid': 'test', 'name': 'test powder'}]
    mocker.patch.object(BaseMaterialService, 'delete_material',
                        autospec=True, return_value=mock_response)

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
