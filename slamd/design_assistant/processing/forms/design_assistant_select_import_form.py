from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators


class DesignAssistantSelectImportForm(Form):
    select_import_field = RadioField(
        label="Design Assitant Import Selection",
        choices=[
            "Yes",
            "No",
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )
