from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.design_assistant_form import DesignAssistantForm
from slamd.design_assistant.processing.forms.task_form import TaskForm


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_form(cls):
        form = DesignAssistantForm()
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = TaskForm()
        return form
    
    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = CampaignForm()
        return form
