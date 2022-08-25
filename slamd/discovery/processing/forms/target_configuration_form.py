from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, RadioField, validators


class TargetConfigurationForm(Form):

    max_or_min = RadioField(
        label='Maximize or minimize target',
        validators=[validators.DataRequired()],
        choices=[
            ('min', 'Minimize'),
            ('max', 'Maximize')
        ]
    )

    weight = DecimalField(
        label='Weight',
        validators=[validators.Optional()]
    )
