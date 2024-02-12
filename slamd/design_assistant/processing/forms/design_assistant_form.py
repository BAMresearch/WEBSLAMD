from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.design_assistant.processing.forms.task_form import (
    TaskForm,
)
from slamd.design_assistant.processing.forms.import_form import (
    ImportForm,
)
from slamd.design_assistant.processing.forms.campaign_form import (
    CampaignForm,
)


class DesignAssistantForm(Form):

    task_form = FormField(TaskForm)

    import_form = FormField(ImportForm)

    campaign_form = FormField(CampaignForm)
