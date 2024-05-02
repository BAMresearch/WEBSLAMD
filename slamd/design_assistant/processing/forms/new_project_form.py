from flask_wtf import FlaskForm as Form
from wtforms import FormField

from slamd.design_assistant.processing.forms.create_powder_form import CreatePowderForm


class NewProjectForm(Form):
    create_powder_form = FormField(CreatePowderForm)
