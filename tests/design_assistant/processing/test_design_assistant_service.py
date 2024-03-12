import pytest

from slamd import create_app
from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.design_assistant_service import DesignAssistantService


def test_update_design_assistant_session_calls_persistence_with_task(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_task_key(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_task_key', mock_update_session_for_task_key)
    DesignAssistantService.update_design_assistant_session('zero_shot_learner', 'task')

    assert mock_update_session_called_with == 'zero_shot_learner'


def test_update_design_assistant_session_raises_error_on_invalid_task():
    with pytest.raises(ValueNotSupportedException):
        DesignAssistantService.update_design_assistant_session('invalid', 'task')


def test_update_design_assistant_session_calls_persistence_with_type(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_type_key(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_material_type_key',
                        mock_update_session_for_type_key)
    DesignAssistantService.update_design_assistant_session('Concrete', 'type')

    assert mock_update_session_called_with == 'Concrete'


def test_update_design_assistant_session_raises_error_on_invalid_type():
    with pytest.raises(ValueNotSupportedException):
        DesignAssistantService.update_design_assistant_session('invalid', 'type')


def test_update_design_assistant_session_calls_persistence_with_targets(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_targets(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_design_targets_key',
                        mock_update_session_for_targets)
    mock_targets = {'x1': 1, 'x2': 2}
    DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')

    assert mock_update_session_called_with == mock_targets


def test_update_design_assistant_session_raises_error_on_too_many_design_targets():
    with pytest.raises(ValueNotSupportedException):
        mock_targets = {'x1': 1, 'x2': 2, 'x3': 3}
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_raises_error_when_values_are_not_numeric():
    with pytest.raises(ValueNotSupportedException):
        mock_targets = {'x1': '', 'x2': 'not numeric'}
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_calls_persistence_with_powders(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_powders(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_powders_key', mock_update_session_for_powders)
    mock_powders = {'blend_powders': 'no', 'selected_powders': ['opc']}
    DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')

    assert mock_update_session_called_with == mock_powders


def test_update_design_assistant_session_raises_error_when_powder_blend_is_invalid():
    with pytest.raises(ValueNotSupportedException):
        mock_powders = {'blend_powders': 'invalid', 'selected_powders': ['opc']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_when_powder_is_invalid():
    with pytest.raises(ValueNotSupportedException):
        mock_powders = {'blend_powders': 'no', 'selected_powders': ['invalid']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_when_one_powder_should_be_blend():
    with pytest.raises(ValueNotSupportedException):
        mock_powders = {'blend_powders': 'yes', 'selected_powders': ['opc']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_with_more_than_two_powder():
    with pytest.raises(ValueNotSupportedException):
        mock_powders = {'blend_powders': 'no', 'selected_powders': ['opc', 'ggbfs', 'fly_ash']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_calls_persistence_with_liquid(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_liquid(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_liquid_key', mock_update_session_for_liquid)
    mock_liquid = 'valid name'
    DesignAssistantService.update_design_assistant_session(mock_liquid, 'liquid')

    assert mock_update_session_called_with == mock_liquid


def test_update_design_assistant_session_raises_error_when_liquid_is_too_long():
    with pytest.raises(ValueNotSupportedException):
        mock_liquid = 'This liquid name is way too long and thus invalid'
        DesignAssistantService.update_design_assistant_session(mock_liquid, 'liquid')


def test_update_design_assistant_session_calls_persistence_with_other(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_other(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_other_key', mock_update_session_for_other)
    mock_other = 'valid name'
    DesignAssistantService.update_design_assistant_session(mock_other, 'other')

    assert mock_update_session_called_with == mock_other


def test_update_design_assistant_session_raises_error_when_other_is_too_long():
    with pytest.raises(ValueNotSupportedException):
        mock_liquid = 'This other name is way too long and thus invalid'
        DesignAssistantService.update_design_assistant_session(mock_liquid, 'other')


def test_create_design_assistant_form_creates_properly_populated_form(monkeypatch):
    mock_get_session_called_with = None

    def mock_get_session_for_property(input):
        nonlocal mock_get_session_called_with
        mock_get_session_called_with = input
        return {'dataset': 'None',
                'zero_shot_learner': {'design_targets': [{'reactivity': ''}, {'cost': ''}], 'liquid': 'dhiwq',
                                      'powders': {'blend': 'yes', 'selected': ['opc', 'fly_ash']}, 'type': 'Binder'}}

    app = create_app('testing', with_session=False)
    with app.test_request_context('/design_assistant'):
        monkeypatch.setattr(DesignAssistantPersistence, 'get_session_for_property', mock_get_session_for_property)
        form = DesignAssistantService.create_design_assistant_form()

    assert mock_get_session_called_with == 'design_assistant'
    assert form.task_form['task_field'].data == 'zero_shot_learner'
    assert form.campaign_form.data == {'additional_design_targets': [],
                                       'additional_liquid': 'dhiwq',
                                       'additional_other': None,
                                       'blend_powders_field': 'yes',
                                       'comment_field': None,
                                       'design_targets_field': ['reactivity', 'cost'],
                                       'liquids_field': None,
                                       'material_type_field': 'Binder',
                                       'other_field': None,
                                       'select_powders_field': ['opc', 'fly_ash'],
                                       'submit_button': False,
                                       'target_cost_field': '',
                                       'target_reactivity_field': '',
                                       'target_strength_field': None,
                                       'target_sustainability_field': None,
                                       'target_workability_field': None}
