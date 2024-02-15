from slamd.design_assistant.processing.design_assistant_factory import (
    DesignAssistantFactory,
)
from slamd.design_assistant.processing.design_assistant_persistence import (
    DesignAssistantPersistence,
)


class DesignAssistantService:

    @classmethod
    def create_design_assistant_form(cls):
        form = DesignAssistantFactory.create_design_assistant_form()
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantFactory.create_design_assistant_task_form()
        return form

    @classmethod
    def create_design_assistant_import_selection_form(cls):
        form = DesignAssistantFactory.create_design_assistant_import_selection_form()
        return form

    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = DesignAssistantFactory.create_design_assistant_campaign_form()
        return form

    @classmethod
    def init_design_assistant_session(cls):
        DesignAssistantPersistence.init_session()

    @classmethod
    def update_design_assistant_session(cls, task):
        DesignAssistantPersistence.update_session(task)
    