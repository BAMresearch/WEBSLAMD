import pytest

from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_service import DesignAssistantService


def test_update_design_assistant_session_raises_error_on_invalid_task():
    with pytest.raises(ValueNotSupportedException) as e:
        DesignAssistantService.update_design_assistant_session('invalid', 'task')


def test_update_design_assistant_session_raises_error_on_invalid_type():
    with pytest.raises(ValueNotSupportedException) as e:
        DesignAssistantService.update_design_assistant_session('invalid', 'type')


def test_update_design_assistant_session_raises_error_on_too_many_design_targets():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_targets = {'x1': 1, 'x2': 2, 'x3': 3}
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_raises_error_when_values_are_not_numeric():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_targets = {'x1': '', 'x2': 'not numeric'}
        DesignAssistantService.update_design_assistant_session(mock_targets, 'design_targets')


def test_update_design_assistant_session_raises_error_when_powder_blend_is_invalid():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_powders = {'blend_powders': 'invalid', 'selected_powders': ['opc']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_when_powder_is_invalid():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_powders = {'blend_powders': 'no', 'selected_powders': ['invalid']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_when_one_powder_should_be_blend():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_powders = {'blend_powders': 'yes', 'selected_powders': ['opc']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_with_more_than_two_powder():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_powders = {'blend_powders': 'no', 'selected_powders': ['opc', 'ggbfs', 'fly_ash']}
        DesignAssistantService.update_design_assistant_session(mock_powders, 'powders')


def test_update_design_assistant_session_raises_error_when_liquid_is_too_long():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_liquid = 'This liquid name is way too long and thus invalid'
        DesignAssistantService.update_design_assistant_session(mock_liquid, 'liquid')


def test_update_design_assistant_session_raises_error_when_other_is_too_long():
    with pytest.raises(ValueNotSupportedException) as e:
        mock_liquid = 'This other name is way too long and thus invalid'
        DesignAssistantService.update_design_assistant_session(mock_liquid, 'other')
