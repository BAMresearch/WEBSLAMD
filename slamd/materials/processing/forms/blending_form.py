from flask_wtf import FlaskForm as Form
from wtforms import StringField, validators, SubmitField, DecimalField


class BlendingForm(Form):
    # TODO: custom validator
    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message='Material name cannot be empty')]
    )

    increment = DecimalField(
        label='Increment (%)'
    )

    submit = SubmitField('Create blended materials')
