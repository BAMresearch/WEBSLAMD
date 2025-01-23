from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import ADMIXTURE_DEFAULT_DENSITY

class AdmixtureForm(MaterialsForm):
    density = DecimalField(
        label='Specific Gravity',
        default=ADMIXTURE_DEFAULT_DENSITY,
        validators=[
                validators.DataRequired(message='Material density cannot be empty')
        ]
    )
