from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreatePowderForm(Form):

    name = StringField(label="Great! We start by creating powders. What kind of powder do you want to add?")

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

    sio_2 = DecimalField(
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