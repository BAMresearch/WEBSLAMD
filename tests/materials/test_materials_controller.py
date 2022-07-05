from slamd import create_app
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.materials_service import MaterialsService


def test_slamd_shows_form_and_table(client, mocker):
    mocker.patch.object(MaterialsService, 'list_all', autospec=True, return_value=[{'name': 'test powder'}])
    response = client.get('/materials')

    assert response.status_code == 200

    assert b'Name' in response.data
    assert b'Material type' in response.data
    assert b'CO2-Footprint' in response.data
    assert b'Costs' in response.data
    assert b'Delivery time' in response.data

    assert b'All base materials' in response.data
    assert b'test powder' in response.data


def test_slamd_selects_powder(client):
    response = client.get('/materials/powder')

    assert response.status_code == 200
    assert 'Fe2O3' in response.json['template']
    assert 'SiO2' in response.json['template']
    assert 'Al2O3' in response.json['template']
    assert 'CaO' in response.json['template']
    assert 'MgO' in response.json['template']
    assert 'Na2O' in response.json['template']
    assert 'K2O' in response.json['template']
    assert 'SO3' in response.json['template']
    assert 'TiO2' in response.json['template']
    assert 'P2O5' in response.json['template']
    assert 'SrO' in response.json['template']
    assert 'Mn2O3' in response.json['template']


def test_slamd_selects_liquid(client):
    response = client.get('/materials/liquid')

    assert response.status_code == 200
    assert 'Na2SiO3' in response.json['template']
    assert 'NaOH' in response.json['template']
    assert 'Na2SiO3 specific' in response.json['template']
    assert 'NaOH specific' in response.json['template']
    assert 'Total solution' in response.json['template']
    assert 'Na2O (I)' in response.json['template']
    assert 'SiO2 (I)' in response.json['template']
    assert 'H2O' in response.json['template']
    assert 'Na2O (dry)' in response.json['template']
    assert 'SiO2 (dry)' in response.json['template']
    assert 'Water' in response.json['template']
    assert 'Total NaOH' in response.json['template']


def test_slamd_selects_aggregates(client):
    response = client.get('/materials/aggregates')

    assert response.status_code == 200
    template = response.json['template']
    assert 'Fine Aggregates' in template
    assert 'Coarse Aggregates' in template
    assert 'Type' in template
    assert 'Grading Curve' in template


def test_slamd_selects_admixture(client):
    response = client.get('/materials/admixture')

    assert response.status_code == 200
    template = response.json['template']
    assert 'Composition' in template
    assert 'Type' in template

def test_slamd_selects_custom(client):
    response = client.get("/materials/custom")
    assert response.status_code == 200
    template = response.json['template']
    assert 'Name' in template
    assert 'Value' in template

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
        mocker.patch.object(MaterialsService, 'save_material', autospec=True, return_value=(True, None))
        form = PowderForm(material_name='test powder', material_type='Powder')

        response = client.post('/materials', data=form.data)

    assert response.status_code == 302
    assert b'test powder' not in response.data
    assert response.request.path == '/materials'
