from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, FieldList, FormField, SubmitField

from slamd.materials.forms.add_property_form import AddPropertyForm


class PowderForm(Form):

    ingredient = DecimalField(
        label='FeO')

    additional_properties = FieldList(FormField(AddPropertyForm),
                                      label='Custom Property',
                                      min_entries=1,
                                      max_entries=10)

    add_button = SubmitField('Add another property')
