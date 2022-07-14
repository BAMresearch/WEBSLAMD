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

        form = BlendedMaterialsService().list_base_material_selection_by_type('powder')

        assert len(form.base_material_selection.choices) == 2
        assert form.base_material_selection.choices[0] == ('test uuid1', 'test powder')
        assert form.base_material_selection.choices[1] == ('test uuid2', 'my powder')


def test_list_material_selection_by_type_raises_not_found_exception():
    with app.test_request_context('/materials/blended/invalid'):
        with pytest.raises(MaterialNotFoundException):
            BlendedMaterialsService().list_base_material_selection_by_type('invalid')


def test_create_ratio_form_creates_all_ratios_for_integer_values():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 45, 'max': 55, 'increment': 5},
                         {'idx': 1, 'min': 2, 'max': 6, 'increment': 2},
                         {'idx': 2, 'min': 53, 'max': 39, 'increment': None}]

        form = BlendedMaterialsService().create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 9
        assert data == [{'ratio': '45/2/53'}, {'ratio': '45/4/51'}, {'ratio': '45/6/49'},
                        {'ratio': '50/2/48'}, {'ratio': '50/4/46'}, {'ratio': '50/6/44'},
                        {'ratio': '55/2/43'}, {'ratio': '55/4/41'}, {'ratio': '55/6/39'}]


def test_create_ratio_form_creates_all_ratios_for_decimal_values():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 10, 'max': 15, 'increment': 5},
                         {'idx': 1, 'min': 90, 'max': 85, 'increment': None}]

        form = BlendedMaterialsService().create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 2
        assert data == [{'ratio': '10/90'}, {'ratio': '15/85'}]


def test_create_ratio_form_creates_all_ratios_for_large_increment_value():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 10, 'max': 15, 'increment': 30},
                         {'idx': 1, 'min': 90, 'max': 85, 'increment': None}]

        form = BlendedMaterialsService().create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 1
        assert data == [{'ratio': '10/90'}]
