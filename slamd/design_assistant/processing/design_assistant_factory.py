from slamd.design_assistant.processing.forms.design_assistant_task_form import DesignAssistantTaskForm
from slamd.design_assistant.processing.forms.design_assistant_select_import_form import DesignAssistantSelectImportForm
from slamd.design_assistant.processing.forms.design_assistant_campaign_form import DesignAssistantCampaignForm

class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = DesignAssistantCampaignForm()
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantTaskForm()
        return form

    @classmethod
    def create_design_assistant_select_import_form(cls):
        form = DesignAssistantSelectImportForm()
        return form
