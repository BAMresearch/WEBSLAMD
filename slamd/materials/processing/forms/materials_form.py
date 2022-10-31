from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms import FieldList, FormField
from wtforms import validators

from slamd.materials.processing.forms.additional_property_form import AdditionalPropertyForm


class MaterialsForm(Form):

    material_name = StringField(
        label='1 - Name *',
        validators=[validators.DataRequired(message='Material name cannot be empty')]
    )

    material_type = SelectField(
        label='2 - Material type / Process *',
        validators=[validators.DataRequired(message='Material type cannot be empty')],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Process', 'Custom']
    )

    co2_footprint = DecimalField(
        label='CO₂ footprint (kg/ton for materials, kg for processes)',
        validators=[
            validators.Optional()
        ]
    )

    costs = DecimalField(
        label='Costs (€/ton'
              ' for materials, € for processes)',
        validators=[
            validators.Optional()
        ]
    )

    delivery_time = DecimalField(
        label='Delivery time (days)',
        validators=[
            validators.Optional(),
            validators.NumberRange(min=0, message='Delivery time must be nonnegative')
        ]
    )

    additional_properties = FieldList(FormField(AdditionalPropertyForm),
                                      label='Custom Properties',
                                      min_entries=0,
                                      max_entries=10)

    submit = SubmitField('Submit')
