from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import validators, SelectMultipleField, SelectField, DecimalRangeField


class DiscoveryForm(Form):

    upload_file = FileField(
        label="CSV File Upload",
        validators=[
            FileRequired(),
            FileAllowed(['csv'], message='Only CSV files are allowed')
        ]
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
        label='A priori Information',
        validators=[validators.DataRequired()],
        choices=[]
    )

    select_model = SelectField(
        label='Select Model',
        validators=[validators.DataRequired()],
        choices=[
            'AI Model (lolo Random Forest)',
            'Statistics-based model (Gaussian Process Regression)'
        ]
    )

    curiosity = DecimalRangeField(
        label='Curiosity (to control the weight of model uncertainty on predicted utility)',
        default=1.00,
        places=2,
        validators=[validators.NumberRange(min=0, max=10, message='The curiosity value should be between 0 and 10')]
    )

    # left - exploit
    # right - explore
    # AI Model LOLO as a built-in
