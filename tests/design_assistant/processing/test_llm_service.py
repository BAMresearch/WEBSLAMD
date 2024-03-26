import os

from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.llm_service import LLMService


def test_update_design_assistant_session_calls_persistence_with_task(monkeypatch):

    def mock_get_free_llm_calls_count():
        return 2

    mock_update_remaining_free_llm_calls_called_with = None

    def mock_update_remaining_free_llm_calls():
        nonlocal mock_update_remaining_free_llm_calls_called_with
        mock_update_remaining_free_llm_calls_called_with = 3
        return None

    monkeypatch.setitem(os.environ, 'OPENAI_API_TOKEN', 'test token')
    monkeypatch.setattr(DesignAssistantPersistence, 'get_free_llm_calls_count', mock_get_free_llm_calls_count)
    monkeypatch.setattr(DesignAssistantPersistence, 'update_remaining_free_llm_calls', mock_update_remaining_free_llm_calls)

    token = LLMService.use_free_tier_token()

    assert token == 'test token'
    assert mock_update_remaining_free_llm_calls_called_with == 3
