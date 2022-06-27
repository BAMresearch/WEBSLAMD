from wtforms import DecimalField, StringField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class AdmixtureForm(BaseMaterialsForm):

    composition = DecimalField(label='Composition')

    type = StringField(label='Type')
