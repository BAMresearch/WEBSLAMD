from slamd.design_assistant.processing.design_assistant_factory import (
    DesignAssistantFactory,
)
from abc import ABC, abstractmethod


class DesignAssistantService:

    @classmethod
    def create_design_assistant_service_form(cls):
        form = DesignAssistantFactory.create_design_assistant_service_form()
        return form
        # print("test")
