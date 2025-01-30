from wtforms import DecimalField, validators


from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import CUSTOM_DEFAULT_SPECIFIC_GRAVITY


class CustomForm(MaterialsForm):
    specific_gravity = DecimalField(
        label='Specific Gravity',
        default=CUSTOM_DEFAULT_SPECIFIC_GRAVITY,
        validators=[
            validators.DataRequired(message='Material specific gravity cannot be empty')
        ]
    )
