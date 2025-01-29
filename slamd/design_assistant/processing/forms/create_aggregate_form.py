from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreateAggregateForm(Form):

    name_field = StringField(label="What kind of aggregate do you want to add?")

    cost_CO_2 = DecimalField(
        'CO2 footprint (kg/ton):',
        validators=[
            validators.Optional()
        ]
    )
    
    cost_EUR = DecimalField(
        'Costs (€/ton):',
        validators=[
            validators.Optional()
        ]
    ) 

    cost_delivery_time = DecimalField(
        'Delivery time (days):',
        validators=[
            validators.Optional()
        ]
    )

    cost_recyclingrate = DecimalField(
        label='Recyclingrate (%)',
        validators=[
            validators.optional()
        ]
    )

    fine_aggregates = DecimalField(
        label='Fine Aggregates (m%)',
        validators=[
            validators.Optional()
        ]
    )

    coarse_aggregates = DecimalField(
        label='Coarse Aggregates (m%)',
        validators=[
            validators.Optional()
        ]
    )

    fineness_modulus = DecimalField(
        label='Fineness modulus (m³/kg)',
        validators=[
            validators.Optional()
        ]
    )

    water_absorption = DecimalField(
        label='Water absorption (m%)',
        validators=[
            validators.Optional()
        ]
    )
