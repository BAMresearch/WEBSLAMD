from flask_wtf import FlaskForm as Form
from wtforms import FormField

from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.task_form import TaskForm
from slamd.design_assistant.processing.forms.material_type_form import MaterialTypeForm
from slamd.design_assistant.processing.forms.token_form import TokenForm
from slamd.design_assistant.processing.forms.new_project_form import NewProjectForm

class DesignAssistantForm(Form):
    token_form = FormField(TokenForm)
    task_form = FormField(TaskForm)
    material_type_form = FormField(MaterialTypeForm)
    campaign_form = FormField(CampaignForm)
    new_project_form = FormField(NewProjectForm)

    

