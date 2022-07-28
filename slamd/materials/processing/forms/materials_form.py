from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms import FieldList, FormField
from wtforms import validators

from slamd.materials.processing.forms.add_property_form import AddPropertyForm


class MaterialsForm(Form):

    material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Material name cannot be empty')]
    )

    material_type = SelectField(
        label='Material type / Process',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Process', 'Custom']
    )

    co2_footprint = DecimalField(
        label='CO₂ footprint (kg)',
        validators=[
            validators.Optional()
        ]
    )

    costs = DecimalField(
        label='Costs (€/kg)',
        validators=[
            validators.Optional()
        ]
    )

    delivery_time = DecimalField(
        label='Delivery time (days)',
        validators=[
            validators.Optional()
        ]
    )

    additional_properties = FieldList(FormField(AddPropertyForm),
                                      label='Custom Properties',
                                      min_entries=0,
                                      max_entries=10)

    submit = SubmitField('Save material')
