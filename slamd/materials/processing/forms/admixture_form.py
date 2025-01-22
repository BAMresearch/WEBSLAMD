from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm


class AdmixtureForm(MaterialsForm):
    density = DecimalField(
        label='Admixture Specific Gravity',
        default=1.50,
        validators=[
                validators.DataRequired(message='Material density cannot be empty')
        ]
    )
