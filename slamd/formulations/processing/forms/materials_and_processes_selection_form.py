from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField


class MaterialsAndProcessesSelectionForm(Form):

    material_selection = SelectMultipleField(
        label='Materials',
        validators=[validators.DataRequired()],
        choices=[]
    )

    process_selection = SelectMultipleField(
        label='Materials',
        validators=[validators.DataRequired()],
        choices=[]
    )

    submit = SubmitField('Create materials formulations')
