from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms import FieldList, FormField
from wtforms import validators, ValidationError

from slamd.materials.forms.validation import name_is_unique
from slamd.materials.forms.add_property_form import AddPropertyForm


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

    additional_properties = FieldList(FormField(AddPropertyForm),
                                      label='Custom Property',
                                      min_entries=1,
                                      max_entries=10)

    submit = SubmitField('Add material')
