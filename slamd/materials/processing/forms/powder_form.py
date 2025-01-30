from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import POWDER_DEFAULT_SPECIFIC_GRAVITY

class PowderForm(MaterialsForm):

    fe3_o2 = DecimalField(
        label='Fe₂O₃ (m%)',
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

    al2_o3 = DecimalField(
        label='Al₂O₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    ca_o = DecimalField(
        label='CaO (m%)',
        validators=[
            validators.Optional()
        ]
    )

    mg_o = DecimalField(
        label='MgO (m%)',
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

    k2_o = DecimalField(
        label='K₂O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    s_o3 = DecimalField(
        label='SO₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    ti_o2 = DecimalField(
        label='TiO₂ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    p2_o5 = DecimalField(
        label='P₂O₅ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    sr_o = DecimalField(
        label='SrO (m%)',
        validators=[
            validators.Optional()
        ]
    )

    mn2_o3 = DecimalField(
        label='Mn₂O₃ (m%)',
        validators=[
            validators.Optional()
        ]
    )

    loi = DecimalField(
        label='LOI (m%)',
        validators=[
            validators.Optional()
        ]
    )

    fine = DecimalField(
        label='Fine modules (m²/kg)',
        validators=[
            validators.Optional()
        ]
    )

    specific_gravity = DecimalField(
        label='Specific Gravity',
        default=POWDER_DEFAULT_SPECIFIC_GRAVITY,
        validators=[
            validators.DataRequired(message='Material specific gravity cannot be empty')
        ]
    )
