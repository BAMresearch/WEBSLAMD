import pytest

from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException
from slamd.materials.processing.blended_materials_service import BlendedMaterialsService
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from tests.materials.materials_test_data import create_test_powders

app = create_app('testing', with_session=False)


def test_list_material_selection_by_type_returns_correct_form(monkeypatch):
    with app.test_request_context('/materials/blended'):
        def mock_query_by_type(input):
            if input == 'powder':
                return create_test_powders()
            return []

        monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

        form = BlendedMaterialsService().list_material_selection_by_type('powder')

        assert len(form.base_material_selection.choices) == 2
        assert form.base_material_selection.choices[0] == ('test uuid1', 'test powder')
        assert form.base_material_selection.choices[1] == ('test uuid2', 'my powder')


def test_list_material_selection_by_type_raises_not_found_exception():
    with app.test_request_context('/materials/blended/invalid'):
        with pytest.raises(MaterialNotFoundException):
            BlendedMaterialsService().list_material_selection_by_type('invalid')
