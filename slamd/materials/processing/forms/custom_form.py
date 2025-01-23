from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import CUSTOM_DEFAULT_DENSITY


class CustomForm(MaterialsForm):
    density = DecimalField(
        label='Specific Gravity',
        default=CUSTOM_DEFAULT_DENSITY,
        validators=[
            validators.DataRequired(message='Material density cannot be empty')
        ]
    )
