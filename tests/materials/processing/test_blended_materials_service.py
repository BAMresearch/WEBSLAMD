import pytest
from unittest.mock import MagicMock
from werkzeug.datastructures import MultiDict

from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException, SlamdRequestTooLargeException, \
    ValueNotSupportedException
from slamd.materials.processing.blended_materials_service import BlendedMaterialsService
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.ratio_parser import RatioParser
from tests.materials.materials_test_data import create_test_powders, prepare_test_base_powders_for_blending, \
    prepare_test_base_aggregates_for_blending, prepare_test_base_liquids_for_blending, create_test_base_materials_dict, \
    create_test_normalized_blending_ratios_for_two_materials

app = create_app('testing', with_session=False)


def test_list_material_selection_by_type_returns_correct_sorted_form(monkeypatch):
    with app.test_request_context('/materials/blended'):
        def mock_query_by_type(input):
            if input == 'powder':
                return create_test_powders()
            return []

        monkeypatch.setattr(MaterialsPersistence, 'query_by_type', mock_query_by_type)

        form = BlendedMaterialsService.list_base_material_selection_by_type('powder')

        assert len(form.base_material_selection.choices) == 2
        assert form.base_material_selection.choices[0] == ('test uuid2', 'my powder')
        assert form.base_material_selection.choices[1] == ('test uuid1', 'test powder')


def test_list_material_selection_by_type_raises_not_found_exception():
    with app.test_request_context('/materials/blended/invalid'):
        with pytest.raises(MaterialNotFoundException):
            BlendedMaterialsService.list_base_material_selection_by_type('invalid')


def test_create_ratio_form_creates_all_ratios_for_integer_values():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 45, 'max': 55, 'increment': 5},
                         {'idx': 1, 'min': 2, 'max': 6, 'increment': 2},
                         {'idx': 2, 'min': 39, 'max': 53, 'increment': 1}]

        form = BlendedMaterialsService.create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 9
        assert data == [{'ratio': '45/2/53'}, {'ratio': '45/4/51'}, {'ratio': '45/6/49'},
                        {'ratio': '50/2/48'}, {'ratio': '50/4/46'}, {'ratio': '50/6/44'},
                        {'ratio': '55/2/43'}, {'ratio': '55/4/41'}, {'ratio': '55/6/39'}]

def test_create_ratio_form_creates_all_ratios_for_decimal_values():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 10, 'max': 15, 'increment': 5},
                         {'idx': 1, 'min': 85, 'max': 90, 'increment': 5}]

        form = BlendedMaterialsService.create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 2
        assert data == [{'ratio': '10/90'}, {'ratio': '15/85'}]


def test_create_ratio_form_raises_exception_when_too_many_ratios_are_requested():
    with app.test_request_context('/materials/blended/add_ratios'):
        with pytest.raises(SlamdRequestTooLargeException):
            ratio_request = [{'idx': 0, 'min': 1, 'max': 99, 'increment': 1},
                             {'idx': 1, 'min': 1, 'max': 99, 'increment': 1},
                             {'idx': 2, 'min': 1, 'max': 99, 'increment': 1}
                             ]

            BlendedMaterialsService.create_ratio_form(ratio_request)


def test_save_blended_materials_throws_exception_when_name_is_not_set():
    with app.test_request_context('/materials/blended'):
        form = MultiDict()
        form.add('base_type', 'Powder')

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService.save_blended_materials(form)


def test_save_blended_materials_throws_exception_when_too_many_ratios_are_passed():
    with app.test_request_context('/materials/blended'):
        form = MultiDict()
        form.add('blended_material_name', 'test blend')
        form.add('base_type', 'Powder')
        number_larger_than_max_allowed_ratios = 150
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/10')

        with pytest.raises(SlamdRequestTooLargeException):
            BlendedMaterialsService.save_blended_materials(form)


def test_save_blended_materials_throws_exception_when_ratios_have_not_enough_pieces():
    with app.test_request_context('/materials/blended'):
        form = _create_basic_submission_data()
        number_larger_than_max_allowed_ratios = 10
        for i in range(0, number_larger_than_max_allowed_ratios):
            form.add(f'all_ratio_entries-{i}-ratio', '10/15/20')

        form['all_ratio_entries-5-ratio'] = '10/15'

        with pytest.raises(ValueNotSupportedException):
            BlendedMaterialsService.save_blended_materials(form)


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
            BlendedMaterialsService.save_blended_materials(form)


def test_creates_min_max_form_creates_forms_and_returns_completeness_information(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return prepare_test_base_powders_for_blending(material_type, uuid)

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)

    with app.test_request_context('/materials/blended/add_min_max_entries/powder/2'):
        form, complete = BlendedMaterialsService.create_min_max_form('powder', 2, ['uuid1', 'uuid2', 'uuid3'])

    assert len(form.all_min_max_entries.data) == 2
    assert form.all_min_max_entries.data[0] == {'uuid_field': None, 'blended_material_name': None, 'increment': None,
                                                'min': None, 'max': None}
    assert form.all_min_max_entries.data[1] == {'uuid_field': None, 'blended_material_name': None, 'increment': None,
                                                'min': None, 'max': None}
    assert complete is False


def test_save_blended_materials_creates_two_powders_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return prepare_test_base_powders_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Powder()
    mock_save_called_with_second_blended_material = Powder()

    def mock_save(material_type, material):
        if material_type == 'powder':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend 1-Weight-based-powder 1/powder 2/powder 3-0.4/0.4/0.2':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-Weight-based-powder 1/powder 2/powder 3-0.4/0.3/0.3':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Powder', 'Weight-based')
        BlendedMaterialsService.save_blended_materials(form)

    _assert_saved_blended_powders(mock_save_called_with_first_blended_material,
                                  mock_save_called_with_second_blended_material)


def test_save_blended_materials_creates_two_aggregates_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return prepare_test_base_aggregates_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Aggregates()
    mock_save_called_with_second_blended_material = Aggregates()

    def mock_save(material_type, material):
        if material_type == 'aggregates':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material

            if material.name == 'test blend 1-Weight-based-aggregate 1/aggregate 2/aggregate 3-0.4/0.4/0.2':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-Weight-based-aggregate 1/aggregate 2/aggregate 3-0.4/0.3/0.3':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Aggregates', 'Weight-based')

        BlendedMaterialsService.save_blended_materials(form)

    _assert_saved_blended_aggregates(mock_save_called_with_first_blended_material,
                                     mock_save_called_with_second_blended_material)


def test_save_blended_materials_creates_two_liquids_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return prepare_test_base_liquids_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Liquid()
    mock_save_called_with_second_blended_material = Liquid()

    def mock_save(material_type, material):
        if material_type == 'liquid':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend 1-Weight-based-liquid 1/liquid 2/liquid 3-0.4/0.4/0.2':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-Weight-based-liquid 1/liquid 2/liquid 3-0.4/0.3/0.3':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Liquid', 'Weight-based')

        BlendedMaterialsService.save_blended_materials(form)

    _assert_saved_blended_liquids(mock_save_called_with_first_blended_material,
                                  mock_save_called_with_second_blended_material)


def _prepare_request_for_successful_blending(material_type, blending_strategy):
    form = MultiDict()
    form.add('blended_material_name', 'test blend 1')
    form.add('base_type', material_type)
    form['blending_strategy'] = blending_strategy
    form['all_ratio_entries-0-ratio'] = '40/40/20'
    form['all_ratio_entries-1-ratio'] = '40/30/30'
    form.setlist('base_material_selection', ['uuid1', 'uuid2', 'uuid3'])
    return form


def _create_basic_submission_data():
    form = MultiDict()
    form.add('blended_material_name', 'test blend')
    form.add('base_type', 'Powder')
    form.setlist('base_material_selection', ['uuid1', 'uuid2', 'uuid3'])
    return form


def _assert_saved_blended_powders(mock_save_called_with_first_blended_material,
                                  mock_save_called_with_second_blended_material):
    assert mock_save_called_with_first_blended_material.composition.fe3_o2 == 14.0
    assert mock_save_called_with_first_blended_material.composition.si_o2 == 6.64
    assert mock_save_called_with_first_blended_material.composition.al2_o3 == 7.0
    assert mock_save_called_with_first_blended_material.composition.na2_o is None
    assert mock_save_called_with_first_blended_material.composition.p2_o5 is None

    assert mock_save_called_with_first_blended_material.costs.co2_footprint == 16.0
    assert mock_save_called_with_first_blended_material.costs.costs == 42.0
    assert mock_save_called_with_first_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_first_blended_material.structure.fine == 70.0

    assert len(mock_save_called_with_first_blended_material.additional_properties) == 3
    assert mock_save_called_with_first_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_first_blended_material.additional_properties[0].value == '4.4'
    assert mock_save_called_with_first_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_first_blended_material.additional_properties[1].value == '0.6'
    assert mock_save_called_with_first_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_first_blended_material.additional_properties[2].value == '0.4'

    assert mock_save_called_with_first_blended_material.blending_ratios == '0.4/0.4/0.2'
    assert mock_save_called_with_first_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']

    assert mock_save_called_with_second_blended_material.composition.fe3_o2 == 13.0
    assert mock_save_called_with_second_blended_material.composition.si_o2 == 6.08
    assert mock_save_called_with_second_blended_material.composition.al2_o3 == 7.0
    assert mock_save_called_with_second_blended_material.composition.na2_o is None
    assert mock_save_called_with_second_blended_material.composition.p2_o5 is None

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 17.0
    assert mock_save_called_with_second_blended_material.costs.costs == 44.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.structure.fine == 65.0

    assert len(mock_save_called_with_second_blended_material.additional_properties) == 3
    assert mock_save_called_with_second_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_second_blended_material.additional_properties[0].value == '5.0'
    assert mock_save_called_with_second_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_second_blended_material.additional_properties[1].value == '0.7'
    assert mock_save_called_with_second_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_second_blended_material.additional_properties[2].value == '0.3'

    assert mock_save_called_with_second_blended_material.blending_ratios == '0.4/0.3/0.3'
    assert mock_save_called_with_second_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']


def _assert_saved_blended_aggregates(mock_save_called_with_first_blended_material,
                                     mock_save_called_with_second_blended_material):
    assert mock_save_called_with_first_blended_material.composition.fine_aggregates == 17.4
    assert mock_save_called_with_first_blended_material.composition.coarse_aggregates == 5.2

    assert mock_save_called_with_first_blended_material.costs.co2_footprint == 26.0
    assert mock_save_called_with_first_blended_material.costs.costs == 36.0
    assert mock_save_called_with_first_blended_material.costs.delivery_time == 40.0

    assert len(mock_save_called_with_first_blended_material.additional_properties) == 3
    assert mock_save_called_with_first_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_first_blended_material.additional_properties[0].value == '3.8'
    assert mock_save_called_with_first_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_first_blended_material.additional_properties[1].value == '0.8'
    assert mock_save_called_with_first_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_first_blended_material.additional_properties[2].value == '0.2'

    assert mock_save_called_with_first_blended_material.blending_ratios == '0.4/0.4/0.2'
    assert mock_save_called_with_first_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']

    assert mock_save_called_with_second_blended_material.composition.fine_aggregates == 18.1
    assert mock_save_called_with_second_blended_material.composition.coarse_aggregates == 5.69

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 32.0
    assert mock_save_called_with_second_blended_material.costs.costs == 35.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.blending_ratios == '0.4/0.3/0.3'
    assert mock_save_called_with_second_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']


def _assert_saved_blended_liquids(mock_save_called_with_first_blended_material,
                                  mock_save_called_with_second_blended_material):
    assert mock_save_called_with_first_blended_material.composition.na2_si_o3 == 17.4
    assert mock_save_called_with_first_blended_material.composition.na_o_h == 5.2
    assert mock_save_called_with_first_blended_material.composition.na2_si_o3_mol == 5.6
    assert mock_save_called_with_first_blended_material.composition.h2_o_mol == 12.0
    assert mock_save_called_with_first_blended_material.composition.na_o_h_mol is None
    assert mock_save_called_with_first_blended_material.composition.na2_o is None
    assert mock_save_called_with_first_blended_material.composition.si_o2 is None
    assert mock_save_called_with_first_blended_material.composition.h2_o is None
    assert mock_save_called_with_first_blended_material.composition.na2_o_mol is None
    assert mock_save_called_with_first_blended_material.composition.si_o2_mol is None

    assert mock_save_called_with_first_blended_material.costs.co2_footprint == 26.0
    assert mock_save_called_with_first_blended_material.costs.costs == 36.0
    assert mock_save_called_with_first_blended_material.costs.delivery_time == 40.0

    assert len(mock_save_called_with_first_blended_material.additional_properties) == 3
    assert mock_save_called_with_first_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_first_blended_material.additional_properties[0].value == '3.8'
    assert mock_save_called_with_first_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_first_blended_material.additional_properties[1].value == '0.8'
    assert mock_save_called_with_first_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_first_blended_material.additional_properties[2].value == '0.2'

    assert mock_save_called_with_first_blended_material.blending_ratios == '0.4/0.4/0.2'
    assert mock_save_called_with_first_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']

    assert mock_save_called_with_second_blended_material.composition.na2_si_o3 == 18.1
    assert mock_save_called_with_second_blended_material.composition.na_o_h == 5.69
    assert mock_save_called_with_second_blended_material.composition.na2_si_o3_mol == 5.8
    assert mock_save_called_with_second_blended_material.composition.h2_o_mol == 12.5
    assert mock_save_called_with_second_blended_material.composition.na_o_h_mol is None
    assert mock_save_called_with_second_blended_material.composition.na2_o is None
    assert mock_save_called_with_second_blended_material.composition.si_o2 is None
    assert mock_save_called_with_second_blended_material.composition.h2_o is None
    assert mock_save_called_with_second_blended_material.composition.na2_o_mol is None
    assert mock_save_called_with_second_blended_material.composition.si_o2_mol is None

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 32.0
    assert mock_save_called_with_second_blended_material.costs.costs == 35.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.blending_ratios == '0.4/0.3/0.3'
    assert mock_save_called_with_second_blended_material.created_from == ['uuid1', 'uuid2', 'uuid3']


def test_delete_material_calls_persistence_and_returns_remaining_materials(monkeypatch):
    mock_delete_by_type_and_uuid_called_with = None

    def mock_delete_by_type_and_uuid(type, uuid):
        nonlocal mock_delete_by_type_and_uuid_called_with
        mock_delete_by_type_and_uuid_called_with = type, uuid
        return None

    def mock_get_all_types():
        return ['powder']

    def mock_query_by_type(input):
        powders = create_test_powders()
        powders[0].is_blended = True
        return powders

    monkeypatch.setattr(MaterialsPersistence,
                        'delete_by_type_and_uuid', mock_delete_by_type_and_uuid)
    monkeypatch.setattr(MaterialType, 'get_all_types', mock_get_all_types)
    monkeypatch.setattr(MaterialsPersistence,
                        'query_by_type', mock_query_by_type)

    result = BlendedMaterialsService.delete_material('powder', 'uuid to delete')

    all_blended_materials = result.all_materials

    assert len(all_blended_materials) == 1

    dto = all_blended_materials[0]
    assert dto.name == 'test powder'
    assert dto.type == 'Powder'
    assert dto.all_properties == 'Fe₂O₃ (m%): 23.3, Specific Gravity: 3, test prop: test value'

    assert result.ctx == 'blended materials'
    assert mock_delete_by_type_and_uuid_called_with == (
        'powder', 'uuid to delete')


def test_weights_to_specific_gravity_ratio(monkeypatch):
    normalized_ratios = create_test_normalized_blending_ratios_for_two_materials()
    base_materials_dict = create_test_base_materials_dict()
    weights_to_specific_gravity_ratios = RatioParser.volume_to_weight_ratios(normalized_ratios, base_materials_dict)

    assert weights_to_specific_gravity_ratios == [[0.36, 0.64], [0.46, 0.54], [0.57, 0.43]]


def test_save_blended_materials_calls_ratio_parser(monkeypatch):

    def mock_query_by_type_and_uuid(material_type, uuid):
        return prepare_test_base_liquids_for_blending(material_type, uuid)

    mock_volume_to_weight_ratios = MagicMock(return_value=[[0.64, 0.22, 0.14], [0.64, 0.20, 0.16]])

    def mock_save(material_type, material):
        return None

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(RatioParser, 'volume_to_weight_ratios', mock_volume_to_weight_ratios)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Liquid', 'Volume-based')
        BlendedMaterialsService.save_blended_materials(form)

    mock_volume_to_weight_ratios.assert_called()