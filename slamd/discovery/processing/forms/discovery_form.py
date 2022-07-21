from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField
from wtforms import FileField


class DiscoveryForm(Form):

    upload_file = FileField('upload_file')

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

    # left - exploit
    # right - explore
    # AI Model LOLO as a built-in