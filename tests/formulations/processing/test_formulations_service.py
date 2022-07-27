import pytest

from slamd import create_app
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.formulations.processing.formulations_service import FormulationsService
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.process import Process

app = create_app('testing', with_session=False)


def test_populate_selection_form_creates_entries_for_all_materials_and_processes(monkeypatch):
    def mock_find_all():
        powder = Powder(name='test powder', type='powder')
        powder.uuid = '1'
        liquid1 = Liquid(name='test liquid 1', type='liquid')
        liquid1.uuid = '2'
        liquid2 = Liquid(name='test liquid 2', type='liquid')
        liquid2.uuid = '3'
        process = Process(name='test process', type='process')
        process.uuid = '4'
        return MaterialsForFormulations(powders=[powder],
                                        aggregates_list=[],
                                        liquids=[liquid1, liquid2],
                                        admixtures=[],
                                        customs=[],
                                        processes=[process])

    monkeypatch.setattr(MaterialsFacade, 'find_all', mock_find_all)

    with app.test_request_context('/materials/formulations'):
        form = FormulationsService.populate_selection_form()
    assert form.powder_selection.choices == [('', ''), ('powder|1', 'test powder')]
    assert form.liquid_selection.choices == [('', ''), ('liquid|2', 'test liquid 1'), ('liquid|3', 'test liquid 2')]
    assert form.aggregates_selection.choices == [('', '')]
    assert form.admixture_selection.choices == [('', '')]
    assert form.custom_selection.choices == []
    assert form.process_selection.choices == [('process|4', 'test process')]


def test_create_formulations_min_max_form_raises_exception_when_materials_count_is_invalid(monkeypatch):
    with app.test_request_context('/materials/formulations'):
        with pytest.raises(ValueNotSupportedException):
            FormulationsService.create_formulations_min_max_form('not a number', '2')


def test_create_formulations_min_max_form_raises_exception_when_processes_count_is_invalid(monkeypatch):
    with app.test_request_context('/materials/formulations'):
        with pytest.raises(ValueNotSupportedException):
            FormulationsService.create_formulations_min_max_form('2', 'not a number')


# No assertions as we only want to make sure that no exceptions are thrown. The actual processing is already checked
# in a corresponding test at the controller level (test_formulations_controller.py)
def test_create_formulations_min_max_form_does_not_raise_exception_when_params_are_valid(monkeypatch):
    with app.test_request_context('/materials/formulations'):
        FormulationsService.create_formulations_min_max_form('1', '2')


# TODO: use facade instead of persistence
def test_create_weights_form_computes_all_weights_in_unconstrained_case(monkeypatch):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context('/materials/formulations/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration':
                    [
                        {'uuid': '1', 'type': 'Powder', 'min': 10, 'max': 20, 'increment': 5},
                        {'uuid': '2', 'type': 'Aggregates', 'min': 30, 'max': 50, 'increment': 20},
                        {'uuid': '3', 'type': 'Custom', 'min': 7, 'max': 17, 'increment': 10}
                    ],
                'weight_constraint': ''
            }

        form, base_names = FormulationsService.create_weights_form(weight_request_data)

        assert base_names == 'test powder 1/test powder 2  |  test aggregate  |  test custom'
        assert form.all_weights_entries.data == [{'idx': '0', 'weights': '2.0/8.0  |  30.0  |  7.0'},
                                                 {'idx': '1', 'weights': '2.0/8.0  |  30.0  |  17.0'},
                                                 {'idx': '2', 'weights': '2.0/8.0  |  50.0  |  7.0'},
                                                 {'idx': '3', 'weights': '2.0/8.0  |  50.0  |  17.0'},
                                                 {'idx': '4', 'weights': '3.0/12.0  |  30.0  |  7.0'},
                                                 {'idx': '5', 'weights': '3.0/12.0  |  30.0  |  17.0'},
                                                 {'idx': '6', 'weights': '3.0/12.0  |  50.0  |  7.0'},
                                                 {'idx': '7', 'weights': '3.0/12.0  |  50.0  |  17.0'},
                                                 {'idx': '8', 'weights': '4.0/16.0  |  30.0  |  7.0'},
                                                 {'idx': '9', 'weights': '4.0/16.0  |  30.0  |  17.0'},
                                                 {'idx': '10', 'weights': '4.0/16.0  |  50.0  |  7.0'},
                                                 {'idx': '11', 'weights': '4.0/16.0  |  50.0  |  17.0'}]


def test_create_weights_form_computes_all_weights_in_constrained_case(monkeypatch):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context('/materials/formulations/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': [
                    {'uuid': '1', 'type': 'Powder', 'min': 18.2, 'max': 40, 'increment': 10.5},
                    {'uuid': '2', 'type': 'Aggregates', 'min': 15.2, 'max': 25, 'increment': 5.1},
                    {'uuid': '3', 'type': 'Custom', 'min': 67.6, 'max': 35, 'increment': None}],
                'weight_constraint': '100'
            }

        form, base_names = FormulationsService.create_weights_form(weight_request_data)

        assert base_names == 'test powder 1/test powder 2  |  test aggregate  |  test custom'
        assert form.all_weights_entries.data == [{'idx': '0', 'weights': '3.64/14.56  |  15.2  |  66.6'},
                                                 {'idx': '1', 'weights': '3.64/14.56  |  20.3  |  61.5'},
                                                 {'idx': '2', 'weights': '5.74/22.96  |  15.2  |  56.1'},
                                                 {'idx': '3', 'weights': '5.74/22.96  |  20.3  |  51.0'},
                                                 {'idx': '4', 'weights': '7.84/31.36  |  15.2  |  45.6'},
                                                 {'idx': '5', 'weights': '7.84/31.36  |  20.3  |  40.5'}]


def test_create_weights_form_raises_exceptions_when_too_many_weights_are_requested(monkeypatch):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context('/materials/formulations/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': [
                    {'uuid': '1', 'type': 'Powder', 'min': 18.2, 'max': 40, 'increment': 0.1},
                    {'uuid': '2', 'type': 'Aggregates', 'min': 15.2, 'max': 25, 'increment': 0.2},
                    {'uuid': '3', 'type': 'Custom', 'min': 67.6, 'max': 35, 'increment': None}],
                'weight_constraint': '100'
            }

        with pytest.raises(SlamdRequestTooLargeException):
            FormulationsService.create_weights_form(weight_request_data)

# noinspection PyTypeChecker
# mock uuid so we do simply use strings instead of actual uuids
def _mock_get_material(material_type, uuid):
    if material_type == 'Powder':
        if uuid == '1':
            powder = Powder(name='test blended powder', type='powder', is_blended=True, blending_ratios='0.2/0.8',
                            created_from=['4', '5'])
            powder.uuid = '1'
            return powder
        elif uuid == '4':
            powder = Powder(name='test powder 1', type='powder')
            powder.uuid = '4'
            return powder
        else:
            powder = Powder(name='test powder 2', type='powder')
            powder.uuid = '5'
            return powder
    elif material_type == 'Aggregates' and uuid == '2':
        aggregates = Aggregates(name='test aggregate', type='aggregates')
        aggregates.uuid = '2'
        return aggregates
    else:
        custom = Custom(name='test custom', type='custom')
        custom.uuid = '3'
        return custom
