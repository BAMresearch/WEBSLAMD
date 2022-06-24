from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, IntegerField, SelectField, FieldList, FormField, validators, SubmitField

from slamd.materials.forms.add_property_form import AddPropertyForm


class BaseMaterialsForm(Form):
    # ToDo: validation -> name must be unique

    material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message="Material name cannot be empty")]
    )

    material_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Additive', 'Process', 'Custom']
    )

    co2_footprint = DecimalField(
        label='CO2-Footprint',
        validators=[
            validators.Optional()
        ])

    costs = DecimalField(
        label='Costs',
        validators=[
            validators.Optional()
        ])

    delivery_time = IntegerField(
        label='Delivery time',
        validators=[
            validators.Optional()
        ])

    submit = SubmitField('Add material')
