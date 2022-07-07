from wtforms import StringField

from slamd.materials.processing.forms.materials_form import MaterialsForm


class CustomForm(MaterialsForm):

    name = StringField(label='Name:')

    value = StringField(label='Value:')
