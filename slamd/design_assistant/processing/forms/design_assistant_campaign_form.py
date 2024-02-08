from flask_wtf import FlaskForm as Form
from wtforms import FieldList
from slamd.design_assistant.processing.forms.design_assistant_select_import_form import DesignAssistantSelectImportForm
from slamd.design_assistant.processing.forms.design_assistant_task_form import DesignAssistantTaskForm


class DesignAssistantCampaignForm(Form):
    design_assistant_campaign = FieldList(
        DesignAssistantTaskForm, DesignAssistantSelectImportForm
    )
