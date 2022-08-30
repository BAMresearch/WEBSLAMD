from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.discovery.processing.forms.field_configuration_form import FieldConfigurationForm


class TargetConfigurationForm(Form):
    target_configurations = FieldList(FormField(FieldConfigurationForm),
                                      label='Target configurations',
                                      min_entries=0)
