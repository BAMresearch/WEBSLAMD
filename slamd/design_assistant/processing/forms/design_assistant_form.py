from flask_wtf import FlaskForm as Form
from wtforms import FormField

from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.task_form import TaskForm
from slamd.design_assistant.processing.forms.token_form import TokenForm


class DesignAssistantForm(Form):
    token_form = FormField(TokenForm)
    task_form = FormField(TaskForm)
    campaign_form = FormField(CampaignForm)
