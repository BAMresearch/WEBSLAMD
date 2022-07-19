from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField


class DiscoveryForm(Form):

    input_features = SelectMultipleField(
        label='Input Features',
        validators=[validators.DataRequired()],
        choices=[]
    )

    target_features = SelectMultipleField(
        label='Target Features',
        validators=[validators.DataRequired()],
        choices=[]
    )

    a_priori_information = SelectMultipleField(
        label='A-Priori Information',
        validators=[validators.DataRequired()],
        choices=[]
    )

