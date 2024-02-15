from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators


class ImportSelectionForm(Form):
    import_selection_field = RadioField(
        label="Do you want to important an existing campaign?",
        choices=[
            "Yes",
            "No",
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )
