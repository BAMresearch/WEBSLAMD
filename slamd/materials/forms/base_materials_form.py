from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, IntegerField, SelectField, validators, SubmitField, ValidationError

from slamd.materials.forms.validation import name_is_unique


class BaseMaterialsForm(Form):

    material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message='Material name cannot be empty'), name_is_unique]
    )

    material_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Additive', 'Process', 'Custom']
    )

    co2_footprint = DecimalField(
        label='CO2-Footprint (kg)',
        validators=[
            validators.Optional()
        ])

    costs = DecimalField(
        label='Costs (€/kg)',
        validators=[
            validators.Optional()
        ])

    delivery_time = IntegerField(
        label='Delivery time (days)',
        validators=[
            validators.Optional()
        ])

    submit = SubmitField('Add material')
