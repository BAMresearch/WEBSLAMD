from slamd.design_assistant.processing.design_assistant_factory import (
    DesignAssistantFactory,
)
from slamd.design_assistant.processing.design_assistant_persistence import (
    DesignAssistantPersistence,
)
from abc import ABC, abstractmethod


class DesignAssistantService:

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantFactory.create_design_assistant_task_form()
        return form

    @classmethod
    def update_design_assistant_chat(cls, userInput):
        if userInput.type == "design_assistant_task_selection":
            DesignAssistantPersistence.set_session_task(userInput.task)
        DesignAssistantPersistence.set_session_interaction_step()
