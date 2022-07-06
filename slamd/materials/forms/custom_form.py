from wtforms import StringField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class CustomForm(BaseMaterialsForm):

    name = StringField(label='Name:')

    value = StringField(label='Value:')
