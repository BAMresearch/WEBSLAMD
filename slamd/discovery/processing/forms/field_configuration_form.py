from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, RadioField, validators


class FieldConfigurationForm(Form):

    max_or_min = RadioField(
        label='Design target',
        validators=[validators.DataRequired(message='Target column must be either increased or decreased')],
        default='max',
        choices=[
            ('max', 'Maximize'),
            ('min', 'Minimize')
        ]
    )

    weight = DecimalField(
        label='Weight',
        default=1.0,
        validators=[validators.DataRequired(message='Weight for the target column cannot be empty')]
    )

    threshold = DecimalField(
        label='Threshold',
        validators=[validators.Optional()]
    )
