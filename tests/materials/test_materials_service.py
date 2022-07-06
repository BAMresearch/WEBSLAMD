from unittest.mock import patch, MagicMock

import pytest
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

from slamd import create_app
from slamd.materials.forms.admixture_form import AdmixtureForm
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.material_type import MaterialType
from slamd.materials.materials_persistence import MaterialsPersistence
from slamd.materials.materials_service import MaterialsService
from slamd.materials.model.additional_property import AdditionalProperty
from slamd.materials.model.powder import Powder, Composition, Structure
from slamd.materials.strategies.aggregates_strategy import AggregatesStrategy
from slamd.materials.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.strategies.powder_strategy import PowderStrategy

app = create_app('testing', with_session=False)


def test_create_material_form_creates_powder():
    with app.test_request_context('/materials/powder'):
        file, form = MaterialsService().create_material_form('powder')
        assert file == 'powder_form.html'
        assert isinstance(form, PowderForm)


def test_create_material_form_creates_liquid():
    with app.test_request_context('/materials/liquid'):
        file, form = MaterialsService().create_material_form('liquid')
        assert file == 'liquid_form.html'
        assert isinstance(form, LiquidForm)


def test_create_material_form_creates_aggregates():
    with app.test_request_context('/materials/aggregates'):
        file, form = MaterialsService().create_material_form('aggregates')
        assert file == 'aggregates_form.html'
        assert isinstance(form, AggregatesForm)


def test_create_material_form_creates_process():
    with app.test_request_context('/materials/process'):
        file, form = MaterialsService().create_material_form('process')
        assert file == 'process_form.html'
        assert isinstance(form, ProcessForm)


def test_create_material_form_creates_admixture():
    with app.test_request_context('/materials/admixture'):
        file, form = MaterialsService().create_material_form('admixture')
        assert file == 'admixture_form.html'
        assert isinstance(form, AdmixtureForm)


def test_create_material_form_raises_bad_request_when_invalid_form_is_requested():
    with app.test_request_context('/materials/invalid'):
        with pytest.raises(NotFound):
            MaterialsService().create_material_form('invalid')


@patch.object(PowderStrategy, 'create_model', MagicMock(return_value=None))
def test_save_material_creates_powder():
    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test powder'),
                                   ('material_type', 'Powder'),
                                   ('co2_footprint', ''),
                                   ('costs', ''),
                                   ('delivery_time', ''),
                                   ('fe3_o2', ''),
                                   ('si_o2', ''),
                                   ('al2_o3', ''),
                                   ('ca_o', ''),
                                   ('mg_o', ''),
                                   ('na2_o', ''),
                                   ('k2_o', ''),
                                   ('s_o3', ''),
                                   ('p2_o5', ''),
                                   ('ti_o2', ''),
                                   ('sr_o', ''),
                                   ('mn2_o3', ''),
                                   ('fine', ''),
                                   ('gravity', ''),
                                   ('submit', 'Add material')])
        MaterialsService().save_material(form)


@patch.object(LiquidStrategy, 'create_model', MagicMock(return_value=None))
def test_save_material_creates_liquid():
    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test liquid'),
                                   ('material_type', 'Liquid'),
                                   ('na2_si_o3', ''),
                                   ('na_o_h', ''),
                                   ('na2_si_o3_specific', ''),
                                   ('na_o_h_specific', ''),
                                   ('total', ''),
                                   ('na2_o', ''),
                                   ('si_o2', ''),
                                   ('h2_o', ''),
                                   ('na2_o_dry', ''),
                                   ('si_o2_dry', ''),
                                   ('water', ''),
                                   ('na_o_h_total', ''),
                                   ('submit', 'Add material')])
        MaterialsService().save_material(form)


@patch.object(AggregatesStrategy, 'create_model', MagicMock(return_value=None))
def test_save_material_creates_aggregates():
    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test aggregates'),
                                   ('material_type', 'Aggregates'),
                                   ('fine_aggregates', ''),
                                   ('coarse_aggregates', ''),
                                   ('fa_density', ''),
                                   ('ca_density', ''),
                                   ('submit', 'Add material')])
        MaterialsService().save_material(form)


@patch.object(AggregatesStrategy, 'create_model', MagicMock(return_value=None))
def test_save_material_creates_process():
    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test process'),
                                   ('material_type', 'Process'),
                                   ('duration', ''),
                                   ('temperature', ''),
                                   ('relative_humidity', ''),
                                   ('submit', 'Add material')])
        MaterialsService().save_material(form)


def test_list_all_creates_all_materials_for_view(monkeypatch):
    def mock_get_all_types():
        return ['powder']

    def mock_query_by_type(input):
        return _create_test_powders()

    monkeypatch.setattr(MaterialType, 'get_all_types', mock_get_all_types)
    monkeypatch.setattr(MaterialsPersistence,
                        'query_by_type', mock_query_by_type)

    result = MaterialsService().list_all()
    assert len(result) == 2

    dto = result[0]
    assert dto.name == 'my powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == ''

    dto = result[1]
    assert dto.name == 'test powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == u'Fe\u2082O\u2083' + \
        ': 23.3, Specific gravity: 12, test prop: test value'


def _create_test_powders():
    powder1 = Powder(Composition(fe3_o2='23.3'),
                     Structure(gravity='12'))
    powder1.name = 'test powder'
    powder1.type = 'Powder'
    powder1.additional_properties = [
        AdditionalProperty(name='test prop', value='test value')]
    powder2 = Powder(Composition(),
                     Structure())
    powder2.name = 'my powder'
    powder2.type = 'Powder'
    powder2.additional_properties = []
    return [powder1, powder2]
