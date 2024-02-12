from slamd.design_assistant.processing.forms.design_assistant_form import DesignAssistantForm
from slamd.design_assistant.processing.forms.design_assistant_select_task_form import DesignAssistantSelectTaskForm
class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_form(cls):
        form = DesignAssistantForm()
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantSelectTaskForm()
        return form