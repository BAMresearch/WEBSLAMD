from wtforms import DecimalField, StringField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class AdmixtureForm(MaterialsForm):

    composition = DecimalField(
        label='Composition',
        validators=[
            validators.Optional()
        ]
    )

    type = StringField(label='Type')
