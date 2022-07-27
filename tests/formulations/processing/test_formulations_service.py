import pytest

from slamd import create_app
from slamd.common.error_handling import ValueNotSupportedException
from slamd.formulations.processing.formulations_service import FormulationsService
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations
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
