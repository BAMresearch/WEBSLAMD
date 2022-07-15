from unittest.mock import patch, MagicMock

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException
from slamd.materials.processing.base_materials_service import BaseMaterialService
from slamd.materials.processing.forms.admixture_form import AdmixtureForm
from slamd.materials.processing.forms.aggregates_form import AggregatesForm
from slamd.materials.processing.forms.custom_form import CustomForm
from slamd.materials.processing.forms.liquid_form import LiquidForm
from slamd.materials.processing.forms.powder_form import PowderForm
from slamd.materials.processing.forms.process_form import ProcessForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.strategies.admixture_strategy import AdmixtureStrategy
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy
from tests.materials.materials_test_data import create_test_powders

app = create_app('testing', with_session=False)


def test_create_material_form_creates_powder():
    with app.test_request_context('/materials/base/powder'):
        file, form = BaseMaterialService().create_material_form('powder')
        assert file == 'powder_form.html'
        assert isinstance(form, PowderForm)


def test_create_material_form_creates_liquid():
    with app.test_request_context('/materials/base/liquid'):
        file, form = BaseMaterialService().create_material_form('liquid')
        assert file == 'liquid_form.html'
        assert isinstance(form, LiquidForm)


def test_create_material_form_creates_aggregates():
    with app.test_request_context('/materials/base/aggregates'):
        file, form = BaseMaterialService().create_material_form('aggregates')
        assert file == 'aggregates_form.html'
        assert isinstance(form, AggregatesForm)


def test_create_material_form_creates_process():
    with app.test_request_context('/materials/base/process'):
        file, form = BaseMaterialService().create_material_form('process')
        assert file == 'process_form.html'
        assert isinstance(form, ProcessForm)


def test_create_material_form_creates_admixture():
    with app.test_request_context('/materials/base/admixture'):
        file, form = BaseMaterialService().create_material_form('admixture')
        assert file == 'admixture_form.html'
        assert isinstance(form, AdmixtureForm)


def test_create_material_form_creates_custom():
    with app.test_request_context('/materials/base/custom'):
        file, form = BaseMaterialService().create_material_form('custom')
        assert file == 'custom_form.html'
        assert isinstance(form, CustomForm)


def test_create_material_form_raises_bad_request_when_invalid_form_is_requested():
    with app.test_request_context('/materials/base/invalid'):
        with pytest.raises(MaterialNotFoundException):
            BaseMaterialService().create_material_form('invalid')


def test_save_material_creates_powder(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(PowderStrategy, 'create_model', mock_create_model)

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
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_save_material_creates_liquid(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(LiquidStrategy, 'create_model', mock_create_model)

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
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_save_material_creates_aggregates(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(AggregatesStrategy, 'create_model', mock_create_model)

    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test aggregates'),
                                   ('material_type', 'Aggregates'),
                                   ('fine_aggregates', ''),
                                   ('coarse_aggregates', ''),
                                   ('fa_density', ''),
                                   ('ca_density', ''),
                                   ('submit', 'Add material')])
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_save_material_creates_process(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(ProcessStrategy, 'create_model', mock_create_model)

    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test process'),
                                   ('material_type', 'Process'),
                                   ('duration', ''),
                                   ('temperature', ''),
                                   ('relative_humidity', ''),
                                   ('submit', 'Add material')])
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_save_material_creates_admixture(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(AdmixtureStrategy, 'create_model', mock_create_model)

    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test admixture'),
                                   ('material_type', 'Admixture'),
                                   ('composition', ''),
                                   ('type', ''),
                                   ('submit', 'Add material')])
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_save_material_creates_custom(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(self, submitted_material, additional_properties):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material, additional_properties
        return None

    monkeypatch.setattr(CustomStrategy, 'create_model', mock_create_model)

    with app.test_request_context('/materials'):
        form = ImmutableMultiDict([('material_name', 'test custom'),
                                   ('material_type', 'Custom'),
                                   ('custom_name', ''),
                                   ('custom_value', ''),
                                   ('submit', 'Add material')])
        BaseMaterialService().save_material(form)

    assert mock_create_model_called_with == (form, [])


def test_list_all_creates_all_materials_for_view(monkeypatch):
    def mock_get_all_types():
        return ['powder']

    mock_query_by_type_called_with = None

    def mock_query_by_type(input):
        nonlocal mock_query_by_type_called_with
        mock_query_by_type_called_with = input
        return create_test_powders()

    monkeypatch.setattr(MaterialType, 'get_all_types', mock_get_all_types)
    monkeypatch.setattr(MaterialsPersistence,
                        'query_by_type', mock_query_by_type)

    result = BaseMaterialService().list_materials(blended=False)

    _assert_test_powders(result.all_materials)
    assert result.ctx == 'base'
    assert mock_query_by_type_called_with == 'powder'


def test_delete_material_calls_persistence_and_returns_remaining_materials(monkeypatch):
    mock_delete_by_type_and_uuid_called_with = None

    def mock_delete_by_type_and_uuid(type, uuid):
        nonlocal mock_delete_by_type_and_uuid_called_with
        mock_delete_by_type_and_uuid_called_with = type, uuid
        return None

    def mock_get_all_types():
        return ['powder']

    def mock_query_by_type(input):
        return create_test_powders()

    monkeypatch.setattr(MaterialsPersistence,
                        'delete_by_type_and_uuid', mock_delete_by_type_and_uuid)
    monkeypatch.setattr(MaterialType, 'get_all_types', mock_get_all_types)
    monkeypatch.setattr(MaterialsPersistence,
                        'query_by_type', mock_query_by_type)

    result = BaseMaterialService().delete_material('powder', 'uuid to delete')

    _assert_test_powders(result.all_materials)
    assert result.ctx == 'base'
    assert mock_delete_by_type_and_uuid_called_with == (
        'powder', 'uuid to delete')


def _assert_test_powders(all_materials):
    assert len(all_materials) == 2

    dto = all_materials[0]
    assert dto.name == 'my powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == ''
    dto = all_materials[1]
    assert dto.name == 'test powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == 'Fe₂O₃: 23.3, Specific gravity: 12, test prop: test value'
