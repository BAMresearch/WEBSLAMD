from wtforms import DecimalField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class PowdersForm(BaseMaterialsForm):

    ingredient = DecimalField(
        label='FeO')
