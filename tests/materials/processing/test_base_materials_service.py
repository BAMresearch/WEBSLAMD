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
        form = BaseMaterialService.create_material_form('powder')
        assert isinstance(form, PowderForm)
        assert form.material_type.data == 'Powder'


def test_create_material_form_creates_liquid():
    with app.test_request_context('/materials/base/liquid'):
        form = BaseMaterialService.create_material_form('liquid')
        assert isinstance(form, LiquidForm)
        assert form.material_type.data == 'Liquid'


def test_create_material_form_creates_aggregates():
    with app.test_request_context('/materials/base/aggregates'):
        form = BaseMaterialService.create_material_form('aggregates')
        assert isinstance(form, AggregatesForm)
        assert form.material_type.data == 'Aggregates'


def test_create_material_form_creates_process():
    with app.test_request_context('/materials/base/process'):
        form = BaseMaterialService.create_material_form('process')
        assert isinstance(form, ProcessForm)
        assert form.material_type.data == 'Process'


def test_create_material_form_creates_admixture():
    with app.test_request_context('/materials/base/admixture'):
        form = BaseMaterialService.create_material_form('admixture')
        assert isinstance(form, AdmixtureForm)
        assert form.material_type.data == 'Admixture'


def test_create_material_form_creates_custom():
    with app.test_request_context('/materials/base/custom'):
        form = BaseMaterialService.create_material_form('custom')
        assert isinstance(form, CustomForm)
        assert form.material_type.data == 'Custom'


def test_create_material_form_raises_bad_request_when_invalid_form_is_requested():
    with app.test_request_context('/materials/base/invalid'):
        with pytest.raises(MaterialNotFoundException):
            BaseMaterialService.create_material_form('invalid')


def test_save_material_creates_powder(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(PowderStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(PowderStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test powder'),
                                   ('material_type', 'Powder'),
                                   ('specific_gravity', '1'),
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
                                   ('loi', ''),
                                   ('fine', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)


    assert mock_create_model_called_with == form


def test_save_material_creates_liquid(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(LiquidStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(LiquidStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test liquid'),
                                   ('material_type', 'Liquid'),
                                   ('na2_si_o3', ''),
                                   ('na_o_h', ''),
                                   ('na2_si_o3_mol', ''),
                                   ('na_o_h_mol', ''),
                                   ('na2_o', ''),
                                   ('si_o2', ''),
                                   ('h2_o', ''),
                                   ('na2_o_mol', ''),
                                   ('si_o2_mol', ''),
                                   ('h2_o_mol', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)

    assert mock_create_model_called_with == form


def test_save_material_creates_aggregates(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(AggregatesStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(AggregatesStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test aggregates'),
                                   ('material_type', 'Aggregates'),
                                   ('specific_gravity', '1'),
                                   ('fine_aggregates', ''),
                                   ('coarse_aggregates', ''),
                                   ('fa_density', ''),
                                   ('ca_density', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)

    assert mock_create_model_called_with == form


def test_save_material_creates_process(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(ProcessStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(ProcessStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test process'),
                                   ('material_type', 'Process'),
                                   ('duration', ''),
                                   ('temperature', ''),
                                   ('relative_humidity', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)

    assert mock_create_model_called_with == form


def test_save_material_creates_admixture(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(AdmixtureStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(AdmixtureStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test admixture'),
                                   ('material_type', 'Admixture'),
                                   ('specific_gravity', '1'),
                                   ('composition', ''),
                                   ('type', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)

    assert mock_create_model_called_with == form


def test_save_material_creates_custom(monkeypatch):
    mock_create_model_called_with = None

    def mock_create_model(submitted_material):
        nonlocal mock_create_model_called_with
        mock_create_model_called_with = submitted_material
        return None

    def mock_save_model(model):
        return None

    monkeypatch.setattr(CustomStrategy, 'create_model', mock_create_model)
    monkeypatch.setattr(CustomStrategy, 'save_model', mock_save_model)

    with app.test_request_context('/materials/base'):
        form = ImmutableMultiDict([('material_name', 'test custom'),
                                   ('material_type', 'Custom'),
                                   ('specific_gravity', '1'),
                                   ('custom_name', ''),
                                   ('custom_value', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.save_material(form)

    assert mock_create_model_called_with == form


def test_edit_material_edits_powder(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(PowderStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(PowderStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/powder/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test powder'),
                                   ('material_type', 'Powder'),
                                   ('specific_gravity', '1'),
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
                                   ('loi', ''),
                                   ('fine', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('powder', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


def test_edit_material_edits_liquid(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(LiquidStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(LiquidStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/liquid/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test liquid'),
                                   ('material_type', 'Liquid'),
                                   ('specific_gravity', '1'),
                                   ('na2_si_o3', ''),
                                   ('na_o_h', ''),
                                   ('na2_si_o3_mol', ''),
                                   ('na_o_h_mol', ''),
                                   ('na2_o', ''),
                                   ('si_o2', ''),
                                   ('h2_o', ''),
                                   ('na2_o_mol', ''),
                                   ('si_o2_mol', ''),
                                   ('h2_o_mol', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('Liquid', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


def test_edit_material_edits_aggregates(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(AggregatesStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(AggregatesStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/aggregates/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test aggregates'),
                                   ('material_type', 'Aggregates'),
                                   ('specific_gravity', '1'),
                                   ('fine_aggregates', ''),
                                   ('coarse_aggregates', ''),
                                   ('fa_density', ''),
                                   ('ca_density', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('Aggregates', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


def test_edit_material_edits_process(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(ProcessStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(ProcessStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/process/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test process'),
                                   ('material_type', 'Process'),
                                   ('duration', ''),
                                   ('temperature', ''),
                                   ('relative_humidity', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('Process', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


def test_edit_material_edits_admixture(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(AdmixtureStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(AdmixtureStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/admixture/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test admixture'),
                                   ('material_type', 'Admixture'),
                                   ('specific_gravity', '1'),
                                   ('composition', ''),
                                   ('type', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('Admixture', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


def test_edit_material_edits_custom(monkeypatch):
    mock_edit_model_called_with = None

    def mock_edit_model(uuid, submitted_material):
        nonlocal mock_edit_model_called_with
        mock_edit_model_called_with = uuid, submitted_material
        return None

    def mock_save_model(model):
        return None

    def mock_delete_material(type, uuid):
        return None

    monkeypatch.setattr(CustomStrategy, 'edit_model', mock_edit_model)
    monkeypatch.setattr(CustomStrategy, 'save_model', mock_save_model)
    monkeypatch.setattr(BaseMaterialService, 'delete_material', mock_delete_material)

    with app.test_request_context('/materials/base/custom/to_be_edited'):
        form = ImmutableMultiDict([('material_name', 'test custom'),
                                   ('material_type', 'Custom'),
                                   ('specific_gravity', '1'),
                                   ('custom_name', ''),
                                   ('custom_value', ''),
                                   ('submit', 'Save material')])
        BaseMaterialService.edit_material('Custom', 'to_be_edited', form)

    assert mock_edit_model_called_with == ('to_be_edited', form)


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

    result = BaseMaterialService.list_materials(blended=False)

    _assert_test_powders(result.all_materials)
    assert result.ctx == 'base materials / processes'
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

    BaseMaterialService.delete_material('powder', 'uuid to delete')

    assert mock_delete_by_type_and_uuid_called_with == ('powder', 'uuid to delete')


def _assert_test_powders(all_materials):
    assert len(all_materials) == 2

    dto = all_materials[0]
    assert dto.name == 'my powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == 'Specific Gravity: 2'
    dto = all_materials[1]
    assert dto.name == 'test powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == 'Fe₂O₃ (m%): 23.3, Specific Gravity: 3, test prop: test value'
