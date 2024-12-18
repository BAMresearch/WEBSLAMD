from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreateLiquidForm(Form):

    name_field = StringField(label="Great! We continue by creating liquids. What kind of liquid do you want to add?")

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

    h2_O = DecimalField(
        label='H₂O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    h2_O_mol = DecimalField(
        label='H₂O (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_si_o3 = DecimalField(
        label='Na₂SiO₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_si_o3_mol = DecimalField(
        label='Na₂SiO₃ (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h = DecimalField(
        label='NaOH (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_mol = DecimalField(
        label='NaOH (mol%)',
        validators=[
            validators.Optional()
        ]
    )