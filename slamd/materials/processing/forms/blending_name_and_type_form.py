from flask_wtf import FlaskForm as Form
from wtforms import StringField, validators, SubmitField, SelectField

from slamd.materials.processing.forms.validation import blending_name_is_unique


class BlendingNameAndTypeForm(Form):

    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(), blending_name_is_unique]
    )

    base_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Process', 'Custom']
    )

    submit = SubmitField('Create blended materials')
