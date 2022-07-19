from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from slamd.materials.processing.forms.add_property_form import AddPropertyForm


class AdditionalPropertiesForm(Form):
    additional_properties = FieldList(FormField(AddPropertyForm),
                                      label='Custom Properties',
                                      min_entries=0,
                                      max_entries=10)
