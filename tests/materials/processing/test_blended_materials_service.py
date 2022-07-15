import pytest
from werkzeug.datastructures import MultiDict

from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException, SlamdRequestTooLargeException, \
    ValueNotSupportedException
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


def test_create_ratio_form_raises_exception_when_too_many_ratios_are_requested():
    with app.test_request_context('/materials/blended/add_ratios'):
        with pytest.raises(SlamdRequestTooLargeException):
            ratio_request = [{'idx': 0, 'min': 10, 'max': 90, 'increment': 0.01},
                             {'idx': 1, 'min': 90, 'max': 10, 'increment': None}]

            BlendedMaterialsService().create_ratio_form(ratio_request)


def test_create_ratio_form_raises_exception_when_min_value_is_invalid():
    with app.test_request_context('/materials/blended/add_ratios'):
        with pytest.raises(ValueNotSupportedException):
            ratio_request = [{'idx': 0, 'min': -2, 'max': 90, 'increment': 0.01},
                             {'idx': 1, 'min': 90, 'max': 10, 'increment': None}]

            BlendedMaterialsService().create_ratio_form(ratio_request)


def test_save_blended_materials_throws_exception_when_name_is_not_set():
    with app.test_request_context('/materials/blended'):
        form = MultiDict()
        form.add('base_type', 'Powder')

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService().save_blended_materials(form)


def test_save_blended_materials_throws_exception_when_too_many_ratios_are_passed():
    with app.test_request_context('/materials/blended'):
        form = MultiDict()
        form.add('blended_material_name', 'test blend')
        form.add('base_type', 'Powder')
        number_larger_than_max_allowed_ratios = 150
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/10')

        with pytest.raises(SlamdRequestTooLargeException):
            BlendedMaterialsService().save_blended_materials(form)


def test_save_blended_materials_throws_exception_when_ratios_have_not_enough_pieces():
    with app.test_request_context('/materials/blended'):
        form = MultiDict()
        form.add('blended_material_name', 'test blend')
        form.add('base_type', 'Powder')
        form.setlist('base_material_selection', ['uuid1', 'uuid2', 'uuid3'])
        number_larger_than_max_allowed_ratios = 10
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/15/20')

        form['all_ratio_entries-5-ratio'] = '10/15'

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService().save_blended_materials(form)
