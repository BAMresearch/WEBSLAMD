from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import LIQUID_DEFAULT_SPECIFIC_GRAVITY

class LiquidForm(MaterialsForm):
    na2_si_o3 = DecimalField(
        label='Na₂SiO₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_si_o3_mol = DecimalField(
        label='Na₂SiO₃ (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h = DecimalField(
        label='NaOH (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_mol = DecimalField(
        label='NaOH (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o = DecimalField(
        label='Na₂O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o_mol = DecimalField(
        label='Na₂O (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2 = DecimalField(
        label='SiO₂ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2_mol = DecimalField(
        label='SiO₂ (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    h2_o = DecimalField(
        label='H₂O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    h2_o_mol = DecimalField(
        label='H₂O (mol%)',
        validators=[
            validators.Optional()
        ]
    )

    specific_gravity = DecimalField(
        label='Liquid Specific Gravity',
        default=LIQUID_DEFAULT_SPECIFIC_GRAVITY,
        validators=[
            validators.DataRequired(message='Material specific gravity cannot be empty')
        ]
    )
