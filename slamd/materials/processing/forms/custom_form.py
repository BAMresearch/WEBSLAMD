from wtforms import StringField

from slamd.materials.processing.forms.materials_form import MaterialsForm


class CustomForm(MaterialsForm):

    custom_name = StringField(label='Name:')

    custom_value = StringField(label='Value:')
