from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreateAdmixtureForm(Form):

    name_field = StringField(label="What kind of admixture do you want to add?")

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