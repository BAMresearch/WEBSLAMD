from flask_wtf import FlaskForm as Form
from wtforms import StringField, validators, SubmitField, DecimalField, SelectField


class BlendingForm(Form):
    # TODO: custom validator
    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message='Material name cannot be empty')]
    )

    base_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Process', 'Custom']
    )

    submit = SubmitField('Create blended materials')
