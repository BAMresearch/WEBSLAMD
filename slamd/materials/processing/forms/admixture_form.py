from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm


class AdmixtureForm(MaterialsForm):
        density = DecimalField(
            label='Bulk density (kg/m³)',
            validators=[
                validators.Optional()
            ]
        )
