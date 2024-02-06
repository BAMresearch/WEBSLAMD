from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators

from slamd.design_assistant.processing.forms.design_assistant_form import DesignAssistantForm

class DesignAssistantServiceForm(DesignAssistantForm):
    design_assistant_service = RadioField(
        label="Design Assitant Service",
        choices=[
            " Create a new Data Set in the digital Lab",
            "Zero shot predictions using LLMs",
        ],
        validators=[validators.DataRequired(message="Service cannot be empty!")],
    )

