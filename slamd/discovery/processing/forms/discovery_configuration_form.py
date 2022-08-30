from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.discovery.processing.forms.target_configuration_form import TargetConfigurationForm


class DiscoveryConfigurationForm(Form):
    target_configurations = FieldList(FormField(TargetConfigurationForm),
                                      label='Target configurations',
                                      min_entries=0)
