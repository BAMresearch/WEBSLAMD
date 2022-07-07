import pytest
from wtforms import ValidationError, StringField, SelectField

from slamd import create_app
from slamd.materials.processing.forms.powder_form import PowderForm
from slamd.materials.processing.forms.validation import name_is_unique
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.powder import Powder


def test_name_is_unique_is_not_successful_when_name_is_already_used(monkeypatch):
    def mock_query_by_type(input):
        powder = Powder()
        powder.name = 'test material'
        return [powder]

    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        test_form = PowderForm(material_type=SelectField(data='Powder'))
        monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

        test_field = StringField()
        test_field.data = 'test material'
        with pytest.raises(ValidationError):
            name_is_unique(test_form, test_field)


def test_name_is_unique_is_successful_when_name_is_not_already_used(monkeypatch):
    """
    No explicit assertion here. That is intentional as we simply want to make sure that no exception is thrown
    """
    def mock_query_by_type(input):
        powder = Powder()
        powder.name = 'test material'
        return [powder]

    app = create_app('testing', with_session=False)

    with app.test_request_context('/materials'):
        test_form = PowderForm(material_type=SelectField(data='Powder'))
        monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

        test_field = StringField()
        test_field.data = 'other material'

        name_is_unique(test_form, test_field)
