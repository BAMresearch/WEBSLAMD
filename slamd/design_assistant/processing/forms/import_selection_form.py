from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators


class ImportSelectionForm(Form):
    import_selection_field = RadioField(
        label="Do you want to important an existing campaign?",
        choices=[
            ("import_data", "Yes -> Use the \'Upload conversation\' button at the top"),
            ("None", "No, I want to start a new campaign"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )
