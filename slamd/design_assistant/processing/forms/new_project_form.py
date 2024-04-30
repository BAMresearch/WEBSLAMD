from flask_wtf import FlaskForm as Form
from wtforms import FormField, FieldList

from slamd.design_assistant.processing.forms.task_form import TaskForm
from slamd.design_assistant.processing.forms.create_powder_form import CreatePowderForm

class NewProjectForm(Form):
    create_powder_form = FormField(CreatePowderForm)
