from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.discovery.processing.forms.field_configuration_form import FieldConfigurationForm


class APrioriInformationConfigurationForm(Form):
    a_priori_information_configurations = FieldList(FormField(FieldConfigurationForm),
                                                    label='A priori information configurations',
                                                    min_entries=0)
