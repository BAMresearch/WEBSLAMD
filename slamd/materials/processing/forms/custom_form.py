from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm


class CustomForm(MaterialsForm):
    density = DecimalField(
        label='Density (kg/m³)',
        default=1.0,
        validators=[
            validators.Optional()
        ]
    )
