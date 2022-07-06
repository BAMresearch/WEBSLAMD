from wtforms import DecimalField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class CustomForm(BaseMaterialsForm):

    name = DecimalField(
        label='Name:',
        validators=[
            validators.Optional()
        ]
    )

    value = DecimalField(
        label='Value:',
        validators=[
            validators.Optional()
        ]
    )
