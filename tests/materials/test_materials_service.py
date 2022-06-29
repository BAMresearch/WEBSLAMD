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
                                   ('feo', ''),
                                   ('sio', ''),
                                   ('alo', ''),
                                   ('alo', ''),
                                   ('cao', ''),
                                   ('mgo', ''),
                                   ('nao', ''),
                                   ('ko', ''),
                                   ('so', ''),
                                   ('po', ''),
                                   ('tio', ''),
                                   ('sro', ''),
                                   ('mno', ''),
                                   ('fine', ''),
                                   ('gravity', ''),
                                   ('submit', 'Add material')])
        MaterialsService().save_material(form)


def test_find_all_creates_all_materials_for_view(monkeypatch):
    def mock_get_all_types():
        return ['powder']

    def mock_find_by_type(input):
        powder = Powder()
        powder.name = 'test powder'
        powder.type = 'Powder'

        powder.composition = Composition(feo='23.3', sio=None)

        powder.structure = Structure(fine=None, gravity='12')
        powder.additional_properties = [AdditionalProperty(name='test prop', value='test value')]
        return [powder]

    monkeypatch.setattr(MaterialType, 'get_all_types', mock_get_all_types)
    monkeypatch.setattr(MaterialsPersistence, 'find_by_type', mock_find_by_type)

    result = MaterialsService().find_all()
    assert len(result) == 1

    dto = result[0]
    assert dto.name == 'test powder'
    assert dto.type == 'Powder'
    assert dto.further_information == u'Fe\u2082O\u2083' + ': 23.3, Specific gravity: 12, test prop: test value'
