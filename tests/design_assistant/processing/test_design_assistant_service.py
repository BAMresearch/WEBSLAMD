import pytest

from slamd import create_app
from slamd.common.error_handling import ValueNotSupportedException, SlamdUnprocessableEntityException
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
    mock_targets = [{'design_target_name_field': 'Workability'}, {'design_target_name_field': 'Reactivity'}]
    DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')

    assert mock_update_session_called_with == mock_targets


def test_update_design_assistant_session_raises_error_on_too_many_design_targets():
    with pytest.raises(ValueNotSupportedException):
        mock_targets = [{'design_target_name_field': 'Workability'},
                        {'design_target_name_field': 'Reactivity'},
                        {'design_target_name_field': 'too many'}]
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_raises_error_when_value_is_too_long():
    with pytest.raises(ValueNotSupportedException):
        mock_targets = [{'design_target_name_field': 'Workability',
                         'design_target_value_field': 'this value field is way too long and therefore not supported',
                         'design_target_optimization_field': 'maximize'}]
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_calls_persistence_with_powders(monkeypatch):
    mock_update_session_called_with = None

    def mock_update_session_for_powders(input):
        nonlocal mock_update_session_called_with
        mock_update_session_called_with = input
        return None

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_powders_key', mock_update_session_for_powders)
    mock_powders = {'blend_powders': 'No', 'selected_powders': ['OPC']}
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

    monkeypatch.setattr(DesignAssistantPersistence, 'update_session_for_liquids_key', mock_update_session_for_liquid)
    mock_liquid = ['valid name']
    DesignAssistantService.update_design_assistant_session(mock_liquid, 'liquids')

    assert mock_update_session_called_with == mock_liquid


def test_update_design_assistant_session_raises_error_when_liquid_is_too_long():
    with pytest.raises(ValueNotSupportedException):
        mock_liquid = 'This liquid name is way too long and thus invalid'
        DesignAssistantService.update_design_assistant_session(mock_liquid, 'liquids')


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


def test_create_design_assistant_form_creates_properly_populated_form_with_targets(monkeypatch):
    mock_get_session_called_with = None

    def mock_get_session_for_property(input):
        nonlocal mock_get_session_called_with
        mock_get_session_called_with = input
        return {'dataset': 'None',
                'zero_shot_learner': {'design_targets': [{'design_target_name_field': 'Workability',
                                                          'design_target_value_field': '10 MPa',
                                                          'design_target_optimization_field': 'maximize'}],
                                      'liquids': ['dhiwq'],
                                      'powders': {'blend': 'Yes', 'selected': ['OPC', 'Fly Ash']}, 'type': 'Binder'}}

    def mock_get_progress(task):
        if task == 'zero_shot_learner':
            return 3
        return None

    app = create_app('testing', with_session=False)
    with app.test_request_context('/design_assistant'):
        monkeypatch.setattr(DesignAssistantPersistence, 'get_session_for_property', mock_get_session_for_property)
        monkeypatch.setattr(DesignAssistantPersistence, 'get_progress', mock_get_progress)
        form, progress = DesignAssistantService.create_design_assistant_form()

    assert progress == 3
    assert mock_get_session_called_with == 'design_assistant'
    assert form.task_form['task_field'].data == 'zero_shot_learner'
    assert form.campaign_form.data == {'additional_liquid': 'dhiwq',
                                       'additional_other': None,
                                       'blend_powders_field': 'Yes',
                                       'comment_field': None,
                                       'design_knowledge_field': None,
                                       'design_targets': [{'design_target_name_field': 'Workability',
                                                           'design_target_optimization_field': 'maximize',
                                                           'design_target_value_field': '10 MPa'}],
                                       'formulation_field': None,
                                       'liquids_field': None,
                                       'other_field': None,
                                       'select_powders_field': ['OPC', 'Fly Ash'],
                                       'standard_design_targets_field': None,
                                       'submit_button': False}


def test_instantiate_da_session_on_upload_zero_shot_data_creation_mutually_exclusive(monkeypatch):
    session_data = {
        'zero_shot_learner': {},
        'data_creation': {}
    }

    mock_delete_session_key_called_with = None

    def mock_delete_session_key(key):
        nonlocal mock_delete_session_key_called_with
        mock_delete_session_key_called_with = key
        return ""

    mock_init_session_called_with = None

    def mock_init_session():
        nonlocal mock_init_session_called_with
        mock_init_session_called_with = 'mock call'
        return ""

    monkeypatch.setattr(DesignAssistantPersistence, 'delete_session_key', mock_delete_session_key)
    monkeypatch.setattr(DesignAssistantPersistence, 'init_session', mock_init_session)

    with pytest.raises(SlamdUnprocessableEntityException):
        DesignAssistantService.instantiate_da_session_on_upload(session_data)
        assert mock_delete_session_key_called_with == 'design_assistant'
        assert mock_init_session_called_with == 'mock call'


def test_instantiate_da_session_on_upload_zero_shot_data(monkeypatch):
    session_data = {
        'zero_shot_learner': {},
    }

    mock_delete_session_key_called_with = None

    def mock_delete_session_key(key):
        nonlocal mock_delete_session_key_called_with
        mock_delete_session_key_called_with = key
        return ""

    mock_init_session_called_with = None

    def mock_init_session():
        nonlocal mock_init_session_called_with
        mock_init_session_called_with = 'mock call'
        return ""

    mock_save_called_with = None

    def mock_save(session, task):
        nonlocal mock_save_called_with
        mock_save_called_with = session, task
        return ""

    monkeypatch.setattr(DesignAssistantPersistence, 'delete_session_key', mock_delete_session_key)
    monkeypatch.setattr(DesignAssistantPersistence, 'init_session', mock_init_session)
    monkeypatch.setattr(DesignAssistantPersistence, 'save', mock_save)

    DesignAssistantService.instantiate_da_session_on_upload(session_data)
    assert mock_delete_session_key_called_with == 'design_assistant'
    assert mock_init_session_called_with == 'mock call'
    assert mock_save_called_with == ({'zero_shot_learner': {}}, 'zero_shot_learner')


def test_instantiate_da_session_on_upload_data_creation_data(monkeypatch):
    session_data = {
        'data_creation': {},
    }

    mock_delete_session_key_called_with = None

    def mock_delete_session_key(key):
        nonlocal mock_delete_session_key_called_with
        mock_delete_session_key_called_with = key
        return ""

    mock_init_session_called_with = None

    def mock_init_session():
        nonlocal mock_init_session_called_with
        mock_init_session_called_with = 'mock call'
        return ""

    mock_save_called_with = None

    def mock_save(session, task):
        nonlocal mock_save_called_with
        mock_save_called_with = session, task
        return ""

    monkeypatch.setattr(DesignAssistantPersistence, 'delete_session_key', mock_delete_session_key)
    monkeypatch.setattr(DesignAssistantPersistence, 'init_session', mock_init_session)
    monkeypatch.setattr(DesignAssistantPersistence, 'save', mock_save)

    DesignAssistantService.instantiate_da_session_on_upload(session_data)
    assert mock_delete_session_key_called_with == 'design_assistant'
    assert mock_init_session_called_with == 'mock call'
    assert mock_save_called_with == ({'data_creation': {}}, 'data_creation')
