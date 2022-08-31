from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SelectField, DecimalRangeField, FieldList, FormField
from slamd.discovery.processing.forms.field_configuration_form import FieldConfigurationForm


class DiscoveryForm(Form):

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

    model = SelectField(
        label='Select Model',
        validators=[validators.DataRequired()],
        choices=[
            'Statistics-based model (Gaussian Process Regression)',
            'AI Model (lolo Random Forest)'
        ]
    )

    curiosity = DecimalRangeField(
        label='Curiosity (to control the weight of model uncertainty on predicted utility)',
        default=1.00,
        places=2,
        validators=[validators.NumberRange(min=0, max=10, message='The curiosity value should be between 0 and 10')]
    )

    target_configurations = FieldList(FormField(FieldConfigurationForm),
                                      label='Target configurations',
                                      min_entries=0)

    a_priori_information_configurations = FieldList(FormField(FieldConfigurationForm),
                                                    label='A priori information configurations',
                                                    min_entries=0)
