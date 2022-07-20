import pytest
from werkzeug.datastructures import MultiDict

import slamd
from slamd import create_app
from slamd.common.error_handling import MaterialNotFoundException, SlamdRequestTooLargeException, \
    ValueNotSupportedException
from slamd.materials.processing.blended_materials_service import BlendedMaterialsService
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Powder, Structure
from tests.materials.materials_test_data import create_test_powders

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
                         {'idx': 2, 'min': 53, 'max': 39, 'increment': None}]

        form = BlendedMaterialsService.create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 9
        assert data == [{'ratio': '45/2/53'}, {'ratio': '45/4/51'}, {'ratio': '45/6/49'},
                        {'ratio': '50/2/48'}, {'ratio': '50/4/46'}, {'ratio': '50/6/44'},
                        {'ratio': '55/2/43'}, {'ratio': '55/4/41'}, {'ratio': '55/6/39'}]


def test_create_ratio_form_creates_all_ratios_for_decimal_values():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 10, 'max': 15, 'increment': 5},
                         {'idx': 1, 'min': 90, 'max': 85, 'increment': None}]

        form = BlendedMaterialsService.create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 2
        assert data == [{'ratio': '10/90'}, {'ratio': '15/85'}]


def test_create_ratio_form_creates_all_ratios_for_large_increment_value():
    with app.test_request_context('/materials/blended/add_ratios'):
        ratio_request = [{'idx': 0, 'min': 10, 'max': 15, 'increment': 30},
                         {'idx': 1, 'min': 90, 'max': 85, 'increment': None}]

        form = BlendedMaterialsService.create_ratio_form(ratio_request)

        data = form.all_ratio_entries.data

        assert len(data) == 1
        assert data == [{'ratio': '10/90'}]


def test_create_ratio_form_raises_exception_when_too_many_ratios_are_requested():
    with app.test_request_context('/materials/blended/add_ratios'):
        with pytest.raises(SlamdRequestTooLargeException):
            ratio_request = [{'idx': 0, 'min': 10, 'max': 90, 'increment': 0.01},
                             {'idx': 1, 'min': 90, 'max': 10, 'increment': None}]

            BlendedMaterialsService.create_ratio_form(ratio_request)


def test_create_ratio_form_raises_exception_when_min_value_is_invalid():
    with app.test_request_context('/materials/blended/add_ratios'):
        with pytest.raises(ValueNotSupportedException):
            ratio_request = [{'idx': 0, 'min': -2, 'max': 90, 'increment': 0.01},
                             {'idx': 1, 'min': 90, 'max': 10, 'increment': None}]

            BlendedMaterialsService.create_ratio_form(ratio_request)


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


def test_save_blended_materials_creates_two_powders_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return _prepare_test_base_powders_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Powder()
    mock_save_called_with_second_blended_material = Powder()

    def mock_save(material_type, material):
        if material_type == 'powder':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend 1-0':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-1':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Powder')

        BlendedMaterialsService().save_blended_materials(form)

        _assert_saved_blended_powders(mock_save_called_with_first_blended_material,
                                      mock_save_called_with_second_blended_material)


def test_save_blended_materials_creates_two_aggregates_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return _prepare_test_base_aggregates_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Aggregates()
    mock_save_called_with_second_blended_material = Aggregates()

    def mock_save(material_type, material):
        if material_type == 'aggregates':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend 1-0':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-1':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Aggregates')

        BlendedMaterialsService().save_blended_materials(form)

        _assert_saved_blended_aggregates(mock_save_called_with_first_blended_material,
                                         mock_save_called_with_second_blended_material)


def test_save_blended_materials_creates_two_liquids_from_three_base_materials(monkeypatch):
    def mock_query_by_type_and_uuid(material_type, uuid):
        return _prepare_test_base_liquids_for_blending(material_type, uuid)

    mock_save_called_with_first_blended_material = Liquid()
    mock_save_called_with_second_blended_material = Liquid()

    def mock_save(material_type, material):
        if material_type == 'liquid':
            nonlocal mock_save_called_with_first_blended_material
            nonlocal mock_save_called_with_second_blended_material
            if material.name == 'test blend 1-0':
                mock_save_called_with_first_blended_material = material
            if material.name == 'test blend 1-1':
                mock_save_called_with_second_blended_material = material

    monkeypatch.setattr(MaterialsPersistence, 'query_by_type_and_uuid', mock_query_by_type_and_uuid)
    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    with app.test_request_context('/materials/blended'):
        form = _prepare_request_for_successful_blending('Liquid')

        BlendedMaterialsService().save_blended_materials(form)

        _assert_saved_blended_liquids(mock_save_called_with_first_blended_material,
                                      mock_save_called_with_second_blended_material)


def _prepare_request_for_successful_blending(material_type):
    form = MultiDict()
    form.add('blended_material_name', 'test blend 1')
    form.add('base_type', material_type)
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


def _prepare_test_base_powders_for_blending(material_type, uuid):
    if material_type == 'Powder':
        if uuid == 'uuid1':
            powder1 = Powder(name='powder 1', type='Powder',
                             costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                             composition=slamd.materials.processing.models.powder.Composition(fe3_o2=10.0, si_o2=4.4,
                                                                                              al2_o3=7, na2_o=11),
                             structure=Structure(fine=50, gravity=10),
                             additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in powder 2'),
                                                    AdditionalProperty(name='Prop4', value='12')])
            powder1.uuid = 'uuid1'
            return powder1
        if uuid == 'uuid2':
            powder2 = Powder(name='powder 2', type='Powder',
                             costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                             composition=slamd.materials.processing.models.powder.Composition(fe3_o2=20.0, al2_o3=7,
                                                                                              si_o2=10),
                             structure=Structure(fine=100),
                             additional_properties=[AdditionalProperty(name='Prop1', value='4'),
                                                    AdditionalProperty(name='Prop2', value='Other Category'),
                                                    AdditionalProperty(name='Prop4', value='No Number')])
            powder2.uuid = 'uuid2'
            return powder2
        if uuid == 'uuid3':
            powder1 = Powder(name='powder 3', type='Powder',
                             costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                             composition=slamd.materials.processing.models.powder.Composition(fe3_o2=10.0, si_o2=4.4,
                                                                                              al2_o3=7, na2_o=11),
                             structure=Structure(fine=50, gravity=10),
                             additional_properties=[AdditionalProperty(name='Prop1', value='10'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in powder 2'),
                                                    AdditionalProperty(name='Prop4', value='10.2')])
            powder1.uuid = 'uuid1'
            return powder1
        return None
    return None


def _prepare_test_base_aggregates_for_blending(material_type, uuid):
    if material_type == 'Aggregates':
        if uuid == 'uuid1':
            aggregates1 = Aggregates(name='aggregate 1', type='Aggregates',
                                     costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                                     composition=slamd.materials.processing.models.aggregates.Composition(
                                         fine_aggregates=10.0, coarse_aggregates=4.4, fa_density=7,
                                         ca_density=11),
                                     additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                            AdditionalProperty(name='Prop2', value='Category'),
                                                            AdditionalProperty(name='Prop3', value='Not in aggregate '
                                                                                                   '3')])
            aggregates1.uuid = 'uuid1'
            return aggregates1
        if uuid == 'uuid2':
            aggregates2 = Aggregates(name='aggregate 2', type='Aggregates',
                                     costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                                     composition=slamd.materials.processing.models.aggregates.Composition(
                                         fine_aggregates=20.0, coarse_aggregates=4.1, fa_density=4,
                                         ca_density=11),
                                     additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                            AdditionalProperty(name='Prop2', value='Category'),
                                                            AdditionalProperty(name='Prop3', value='Not in aggregate '
                                                                                                   '1')])
            aggregates2.uuid = 'uuid2'
            return aggregates2
        if uuid == 'uuid3':
            aggregates3 = Aggregates(name='aggregate 3', type='Aggregates',
                                     costs=Costs(co2_footprint=70, costs=20, delivery_time=40),
                                     composition=slamd.materials.processing.models.aggregates.Composition(
                                         fine_aggregates=27.0, coarse_aggregates=9.0, fa_density=6,
                                         ca_density=16),
                                     additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                            AdditionalProperty(name='Prop2', value='Category'),
                                                            AdditionalProperty(name='Prop3', value='Not in aggregate '
                                                                                                   '2')])
            aggregates3.uuid = 'uuid3'
            return aggregates3
        return None
    return None


def _prepare_test_base_liquids_for_blending(material_type, uuid):
    if material_type == 'Liquid':
        if uuid == 'uuid1':
            liquid1 = Liquid(name='liquid 1', type='Liquid',
                             costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                             composition=slamd.materials.processing.models.liquid.Composition(
                                 na2_si_o3=10.0, na_o_h=4.4, na2_si_o3_specific=7,
                                 water=11),
                             additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in liquid '
                                                                                           '3')])
            liquid1.uuid = 'uuid1'
            return liquid1
        if uuid == 'uuid2':
            liquid2 = Liquid(name='liquid 2', type='Liquid',
                             costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                             composition=slamd.materials.processing.models.liquid.Composition(
                                 na2_si_o3=20.0, na_o_h=4.1, na2_si_o3_specific=4,
                                 water=11),
                             additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in liquid '
                                                                                           '1')])
            liquid2.uuid = 'uuid2'
            return liquid2
        if uuid == 'uuid3':
            liquid3 = Liquid(name='liquid 3', type='Liquid',
                             costs=Costs(co2_footprint=70, costs=20, delivery_time=40),
                             composition=slamd.materials.processing.models.liquid.Composition(
                                 na2_si_o3=27.0, na_o_h=9.0, na2_si_o3_specific=6,
                                 water=16),
                             additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                    AdditionalProperty(name='Prop2', value='Category'),
                                                    AdditionalProperty(name='Prop3', value='Not in liquid '
                                                                                           '2')])
            liquid3.uuid = 'uuid3'
            return liquid3
        return None
    return None


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
    assert mock_save_called_with_first_blended_material.structure.gravity is None

    assert len(mock_save_called_with_first_blended_material.additional_properties) == 3
    assert mock_save_called_with_first_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_first_blended_material.additional_properties[0].value == '4.4'
    assert mock_save_called_with_first_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_first_blended_material.additional_properties[1].value == '0.6'
    assert mock_save_called_with_first_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_first_blended_material.additional_properties[2].value == '0.4'

    assert mock_save_called_with_second_blended_material.composition.fe3_o2 == 13.0
    assert mock_save_called_with_second_blended_material.composition.si_o2 == 6.08
    assert mock_save_called_with_second_blended_material.composition.al2_o3 == 7.0
    assert mock_save_called_with_second_blended_material.composition.na2_o is None
    assert mock_save_called_with_second_blended_material.composition.p2_o5 is None

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 17.0
    assert mock_save_called_with_second_blended_material.costs.costs == 44.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.structure.fine == 65.0
    assert mock_save_called_with_second_blended_material.structure.gravity is None

    assert len(mock_save_called_with_second_blended_material.additional_properties) == 3
    assert mock_save_called_with_second_blended_material.additional_properties[0].name == 'Prop1'
    assert mock_save_called_with_second_blended_material.additional_properties[0].value == '5.0'
    assert mock_save_called_with_second_blended_material.additional_properties[1].name == 'Category'
    assert mock_save_called_with_second_blended_material.additional_properties[1].value == '0.7'
    assert mock_save_called_with_second_blended_material.additional_properties[2].name == 'Other Category'
    assert mock_save_called_with_second_blended_material.additional_properties[2].value == '0.3'


def _assert_saved_blended_aggregates(mock_save_called_with_first_blended_material,
                                     mock_save_called_with_second_blended_material):
    assert mock_save_called_with_first_blended_material.composition.fine_aggregates == 17.4
    assert mock_save_called_with_first_blended_material.composition.coarse_aggregates == 5.2
    assert mock_save_called_with_first_blended_material.composition.fa_density == 5.6
    assert mock_save_called_with_first_blended_material.composition.ca_density == 12.0

    assert mock_save_called_with_first_blended_material.costs.co2_footprint == 26.0
    assert mock_save_called_with_first_blended_material.costs.costs == 36.0
    assert mock_save_called_with_first_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.composition.fine_aggregates == 18.1
    assert mock_save_called_with_second_blended_material.composition.coarse_aggregates == 5.69
    assert mock_save_called_with_second_blended_material.composition.fa_density == 5.8
    assert mock_save_called_with_second_blended_material.composition.ca_density == 12.5

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 32.0
    assert mock_save_called_with_second_blended_material.costs.costs == 35.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0


def _assert_saved_blended_liquids(mock_save_called_with_first_blended_material,
                                  mock_save_called_with_second_blended_material):
    assert mock_save_called_with_first_blended_material.composition.na2_si_o3 == 17.4
    assert mock_save_called_with_first_blended_material.composition.na_o_h == 5.2
    assert mock_save_called_with_first_blended_material.composition.na2_si_o3_specific == 5.6
    assert mock_save_called_with_first_blended_material.composition.water == 12.0
    assert mock_save_called_with_first_blended_material.composition.na_o_h_specific is None
    assert mock_save_called_with_first_blended_material.composition.total is None
    assert mock_save_called_with_first_blended_material.composition.na2_o is None
    assert mock_save_called_with_first_blended_material.composition.si_o2 is None
    assert mock_save_called_with_first_blended_material.composition.h2_o is None
    assert mock_save_called_with_first_blended_material.composition.na2_o_dry is None
    assert mock_save_called_with_first_blended_material.composition.si_o2_dry is None
    assert mock_save_called_with_first_blended_material.composition.na_o_h_total is None

    assert mock_save_called_with_first_blended_material.costs.co2_footprint == 26.0
    assert mock_save_called_with_first_blended_material.costs.costs == 36.0
    assert mock_save_called_with_first_blended_material.costs.delivery_time == 40.0

    assert mock_save_called_with_second_blended_material.composition.na2_si_o3 == 18.1
    assert mock_save_called_with_second_blended_material.composition.na_o_h == 5.69
    assert mock_save_called_with_second_blended_material.composition.na2_si_o3_specific == 5.8
    assert mock_save_called_with_second_blended_material.composition.water == 12.5
    assert mock_save_called_with_second_blended_material.composition.na_o_h_specific is None
    assert mock_save_called_with_second_blended_material.composition.total is None
    assert mock_save_called_with_second_blended_material.composition.na2_o is None
    assert mock_save_called_with_second_blended_material.composition.si_o2 is None
    assert mock_save_called_with_second_blended_material.composition.h2_o is None
    assert mock_save_called_with_second_blended_material.composition.na2_o_dry is None
    assert mock_save_called_with_second_blended_material.composition.si_o2_dry is None
    assert mock_save_called_with_second_blended_material.composition.na_o_h_total is None

    assert mock_save_called_with_second_blended_material.costs.co2_footprint == 32.0
    assert mock_save_called_with_second_blended_material.costs.costs == 35.0
    assert mock_save_called_with_second_blended_material.costs.delivery_time == 40.0


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
    assert dto.all_properties == 'Fe₂O₃: 23.3, Specific gravity: 12, test prop: test value'

    assert result.ctx == 'blended'
    assert mock_delete_by_type_and_uuid_called_with == (
        'powder', 'uuid to delete')
