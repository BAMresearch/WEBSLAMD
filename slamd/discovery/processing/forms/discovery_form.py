from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, SelectField, DecimalField, DecimalRangeField

from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import NumberRange


class DiscoveryForm(Form):
    upload_file = FileField(
        label="",
        validators=[FileRequired(), FileAllowed(['csv', 'CSVs only!'])]
    )



    select_model = SelectField(
        label='Select Model',
        validators=[validators.DataRequired()],
        choices=['AI-Model (lolo Random Forrest', 'Statistics based model (Gaussian Process Regression)']
    )

    materials_data_input = SelectMultipleField(
        label='Materials Data (Input)',
        validators=[validators.DataRequired()],
        choices=[]
    )

    target_properties = SelectMultipleField(
        label='Target Properties',
        validators=[validators.DataRequired()],
        choices=[]
    )

    a_priori_information = SelectMultipleField(
        label='A-priori Information',
        validators=[validators.DataRequired()],
        choices=[]
    )

    curiosity = DecimalRangeField('Curiosity (to control the weight of model uncertainty on predicted utility)',
                                  default=0)



    # left - exploit
    # right - explore
    # AI Model LOLO as a built-in
