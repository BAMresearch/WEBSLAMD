from flask_wtf import FlaskForm as Form
from wtforms import FormField

from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.task_form import TaskForm



class DesignAssistantForm(Form):
    task_form = FormField(TaskForm)
    campaign_form = FormField(CampaignForm)

