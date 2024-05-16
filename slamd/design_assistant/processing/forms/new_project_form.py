from flask_wtf import FlaskForm as Form
from wtforms import FormField

from slamd.design_assistant.processing.forms.create_powder_form import CreatePowderForm
from slamd.design_assistant.processing.forms.create_liquid_form import CreateLiquidForm
from slamd.design_assistant.processing.forms.create_aggregate_form import CreateAggregateForm
from slamd.design_assistant.processing.forms.create_admixture_form import CreateAdmixtureForm
from slamd.design_assistant.processing.forms.create_process_form import CreateProcessForm

class NewProjectForm(Form):
    create_powder_form = FormField(CreatePowderForm)
    create_liquid_form = FormField(CreateLiquidForm)
    create_aggregate_form = FormField(CreateAggregateForm)
    create_admixture_form = FormField(CreateAdmixtureForm)
    create_process_form = FormField(CreateProcessForm) 
