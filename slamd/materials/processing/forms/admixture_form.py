from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm


class AdmixtureForm(MaterialsForm):
        density = DecimalField(
            label='Admixture density (t/m³)',
            default=1.1,
            validators=[
                validators.Optional()
            ]
        )
