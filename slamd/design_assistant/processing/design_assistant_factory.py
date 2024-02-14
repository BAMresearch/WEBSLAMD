from slamd.design_assistant.processing.forms.design_assistant_form import (
    DesignAssistantForm,
)
from slamd.design_assistant.processing.forms.task_form import TaskForm
from slamd.design_assistant.processing.forms.import_form import ImportForm
from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from flask import session


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_form(cls, session):
        form = DesignAssistantForm(session)
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = TaskForm()
        return form
    
    @classmethod
    def create_design_assistant_import_form(cls):
        form = ImportForm()
        return form
    
    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = CampaignForm()
        return form
