import pytest
from slamd.design_assistant.processing import design_assistant_persistence


def test_update_session_zero_shot_learner(monkeypatch):
    session = {}
    monkeypatch.setattr(design_assistant_persistence, "session", session)

    design_assistant_persistence.DesignAssistantPersistence.update_session("zero_shot_learner", None)

    assert session.get('design_assistant', {}).get('zero_shot_learner') == {}


def test_update_session_type(monkeypatch):
    session = {}
    monkeypatch.setattr(design_assistant_persistence, "session", session)

    design_assistant_persistence.DesignAssistantPersistence.update_session("some_type", "type")

    assert session.get('design_assistant', {}).get('zero_shot_learner', {}).get('type') == "some_type"


@pytest.mark.parametrize(
    "value,expected_result",
    [
        (
                {"key1": "val1", "key2": "val2"},
                [{"key1": "val1"}, {"key2": "val2"}]
        )
    ],
)
def test_update_session_design_targets_dict(value, expected_result, monkeypatch):
    session = {}
    monkeypatch.setattr(design_assistant_persistence, "session", session)

    design_assistant_persistence.DesignAssistantPersistence.update_session(value, "design_targets")

    assert session.get('design_assistant', {}).get('zero_shot_learner', {}).get('design_targets') == expected_result

# You can continue defining more tests similar to these for each key used in the method.
