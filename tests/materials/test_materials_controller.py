from slamd import create_app
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.materials_service import MaterialsService


def test_slamd_shows_form_and_table(client, mocker):
    mocker.patch.object(MaterialsService, 'list_all',
                        autospec=True, return_value=[{'name': 'test powder'}])
    response = client.get('/materials')

    assert response.status_code == 200

    assert b'Name' in response.data
    assert b'Material type' in response.data
    assert bytes('CO₂ footprint', 'utf-8') in response.data
    assert b'Costs' in response.data
    assert b'Delivery time' in response.data

    assert b'All base materials' in response.data
    assert b'test powder' in response.data


def test_slamd_selects_powder(client):
    response = client.get('/materials/powder')

    assert response.status_code == 200
    assert 'Fe₂O₃' in response.json['template']
    assert 'SiO₂' in response.json['template']
    assert 'Al₂O₃' in response.json['template']
    assert 'CaO' in response.json['template']
    assert 'MgO' in response.json['template']
    assert 'Na₂O' in response.json['template']
    assert 'K₂O' in response.json['template']
    assert 'SO₃' in response.json['template']
    assert 'TiO₂' in response.json['template']
    assert 'P₂O₅' in response.json['template']
    assert 'SrO' in response.json['template']
    assert 'Mn₂O₃' in response.json['template']


def test_slamd_selects_liquid(client):
    response = client.get('/materials/liquid')

    assert response.status_code == 200
    assert 'Na₂SiO₃' in response.json['template']
    assert 'NaOH' in response.json['template']
    assert 'Na₂SiO₃ specific' in response.json['template']
    assert 'NaOH specific' in response.json['template']
    assert 'Total solution' in response.json['template']
    assert 'Na₂O (I)' in response.json['template']
    assert 'SiO₂ (I)' in response.json['template']
    assert 'H₂O' in response.json['template']
    assert 'Na₂O (dry)' in response.json['template']
    assert 'SiO₂ (dry)' in response.json['template']
    assert 'Water' in response.json['template']
    assert 'Total NaOH' in response.json['template']


def test_slamd_selects_aggregates(client):
    response = client.get('/materials/aggregates')

    assert response.status_code == 200
    template = response.json['template']
    assert 'Fine Aggregates' in template
    assert 'Coarse Aggregates' in template
    assert 'FA Density' in template
    assert 'CA Density' in template


def test_slamd_selects_admixture(client):
    response = client.get('/materials/admixture')

    assert response.status_code == 200
    template = response.json['template']
    assert 'Composition' in template
    assert 'Type' in template


def test_slamd_selects_process(client):
    response = client.get('/materials/process')

    template = response.json['template']
    assert response.status_code == 200
    assert 'Duration' in template
    assert 'Temperature' in template
    assert 'Relative Humidity' in template


def test_slamd_creates_new_powder_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        mocker.patch.object(MaterialsService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = PowderForm(material_name='test powder', material_type='Powder')

        response = client.post('/materials', data=form.data)

    assert response.status_code == 302
    assert b'test powder' not in response.data
    assert response.request.path == '/materials'


def test_slamd_creates_new_liquid_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        mocker.patch.object(MaterialsService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = LiquidForm(material_name='test liquid', material_type='Liquid')

        response = client.post('/materials', data=form.data)

    assert response.status_code == 302
    assert b'test liquid' not in response.data
    assert response.request.path == '/materials'


def test_slamd_creates_new_aggregates_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        mocker.patch.object(MaterialsService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = AggregatesForm(
            material_name='test aggregates', material_type='Aggregates')

        response = client.post('/materials', data=form.data)

    assert response.status_code == 302
    assert b'test aggregates' not in response.data
    assert response.request.path == '/materials'


def test_slamd_creates_new_process_when_saving_is_successful(client, mocker):
    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        mocker.patch.object(MaterialsService, 'save_material',
                            autospec=True, return_value=(True, None))
        form = ProcessForm(
            material_name='test process', material_type='Process')

        response = client.post('/materials', data=form.data)

    assert response.status_code == 302
    assert b'test process' not in response.data
    assert response.request.path == '/materials'
