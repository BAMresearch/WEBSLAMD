import pytest
from werkzeug.datastructures import MultiDict

from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException, SlamdRequestTooLargeException, \
    ValueNotSupportedException
from slamd.materials.processing.blended_materials_service import BlendedMaterialsService
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Powder, Composition
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
        form = _create_basic_submission_data()
        number_larger_than_max_allowed_ratios = 10
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/15/20')

        form['all_ratio_entries-5-ratio'] = '10/15'

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService().save_blended_materials(form)


def test_save_blended_materials_throws_exception_when_ratios_contain_non_numeric_parts():
    with app.test_request_context('/materials/blended'):
        form = _create_basic_submission_data()
        number_larger_than_max_allowed_ratios = 10
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/15/20')

        form['all_ratio_entries-5-ratio'] = '10.3/15/20'
        form['all_ratio_entries-6-ratio'] = '10/15,7/8'
        form['all_ratio_entries-7-ratio'] = '10/ab/8'

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService().save_blended_materials(form)


def test_save_blended_materials_creates_two_ratios(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return _prepare_test_base_materials_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Powder()
    mock_save_called_with_second_blended_material = Powder()

    def mock_save(material_type, material):
        if material_type == 'powder':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend-0':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend-1':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_succesful_blending()

        BlendedMaterialsService().save_blended_materials(form)

        assert mock_save_called_with_first_blended_material.composition.fe3_o2 == 15.0
        assert mock_save_called_with_first_blended_material.composition.si_o2 == 7.2
        assert mock_save_called_with_first_blended_material.composition.na2_o == None

        assert mock_save_called_with_second_blended_material.composition.fe3_o2 == 17.5
        assert mock_save_called_with_second_blended_material.composition.si_o2 == 8.5
        assert mock_save_called_with_second_blended_material.composition.na2_o == None


def _prepare_request_for_succesful_blending():
    form = MultiDict()
    form.add('blended_material_name', 'test blend')
    form.add('base_type', 'Powder')
    form.setlist('base_material_selection', ['uuid1', 'uuid2'])
    form['all_ratio_entries-0-ratio'] = '50/50'
    form['all_ratio_entries-1-ratio'] = '25/75'
    return form


def _create_basic_submission_data():
    form = MultiDict()
    form.add('blended_material_name', 'test blend')
    form.add('base_type', 'Powder')
    form.setlist('base_material_selection', ['uuid1', 'uuid2', 'uuid3'])
    return form


def _prepare_test_base_materials_for_blending(material_type, uuid):
    if material_type == 'Powder':
        if uuid == 'uuid1':
            powder1 = Powder(name='powder 1', type='Powder', costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                             composition=Composition(fe3_o2=10.0, si_o2=4.4, na2_o=11),
                             additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in powder 2')])
            powder1.uuid = 'uuid1'
            return powder1
        if uuid == 'uuid2':
            powder2 = Powder(name='powder 2', type='Powder', costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                             composition=Composition(fe3_o2=20.0, si_o2=10),
                             additional_properties=[AdditionalProperty(name='Prop1', value='4'),
                                                    AdditionalProperty(name='Prop2', value='Other Category')])
            powder2.uuid = 'uuid2'
            return powder2
        return None
    return None
