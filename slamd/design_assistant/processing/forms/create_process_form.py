from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreateProcessForm(Form):

    name_field = StringField(label="What kind of process do you want to add?")

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

    duration = DecimalField(
        label='Duration (days)',
        validators=[
            validators.Optional()
        ]
    )

    temperature = DecimalField(
        label='Temperature (°C)',
        validators=[
            validators.Optional()
        ]
    )

    relative_humidity = DecimalField(
        label='Relative Humidity (%)',
        validators=[
            validators.Optional()
        ]
    )
