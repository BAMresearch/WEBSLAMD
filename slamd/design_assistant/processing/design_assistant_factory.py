from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.design_assistant_form import DesignAssistantForm
from slamd.design_assistant.processing.forms.import_selection_form import ImportSelectionForm


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_form(cls):
        form = DesignAssistantForm()
        return form

    @classmethod
    def create_design_assistant_import_selection_form(cls):
        form = ImportSelectionForm()
        return form
    
    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = CampaignForm()
        return form