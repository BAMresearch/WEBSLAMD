from slamd.design_assistant.processing.forms.design_assistant_task_form import (
    DesignAssistantTaskForm,
)


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantTaskForm()
        return form
