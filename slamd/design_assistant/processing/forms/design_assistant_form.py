from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.design_assistant.processing.forms.design_assistant_select_task_form import (
    DesignAssistantSelectTaskForm,
)
from slamd.design_assistant.processing.forms.design_assistant_select_import_form import (
    DesignAssistantSelectImportForm,
)
from slamd.design_assistant.processing.forms.design_assistant_campaign_form import (
    DesignAssistantCampaignForm,
)


class DesignAssistantForm(Form):

    select_task_form = FormField(DesignAssistantSelectTaskForm)

    select_import_form = FormField(DesignAssistantSelectImportForm)

    design_assistant_campaign_form = FormField(DesignAssistantCampaignForm)
