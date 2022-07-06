from wtforms import DecimalField, StringField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class AdmixtureForm(BaseMaterialsForm):

    composition = DecimalField(
        label='Composition',
        validators=[
            validators.Optional()
        ]
    )

    type = StringField(label='Type')
