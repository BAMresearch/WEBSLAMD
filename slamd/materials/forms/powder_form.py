from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, FieldList, FormField

from slamd.materials.forms.add_property_form import AddPropertyForm


class PowderForm(Form):

    ingredient = DecimalField(
        label='FeO')

    additional_properties = FieldList(FormField(AddPropertyForm),
                                      label='Custom Property',
                                      min_entries=2,
                                      max_entries=10)
