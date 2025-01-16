from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreatePowderForm(Form):

    name_field = StringField(label="Great! We start by creating powders. What kind of powder do you want to add?")

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
    
    ca_o = DecimalField(
        label='CaO (m%)',
        validators=[
            validators.Optional()
        ]
    )

    al2_o3 = DecimalField(
        label='Al₂O₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2 = DecimalField(
        label='SiO₂',
        validators=[
            validators.Optional()
        ]
    )
    
    Fe_2O_3 = DecimalField(
        label='Fe₂O₃',
        validators=[
            validators.Optional()
        ]
    )

    fines_modulus = DecimalField(
        label='Fines Modulus (m^2/kg):',
        validators=[
            validators.Optional()
        ]
    )

    specific_gravity = DecimalField(
        label='Specific Gravity:',
        validators=[
            validators.Optional()
        ]
    )
