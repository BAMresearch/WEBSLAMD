from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class LiquidForm(MaterialsForm):
    na2_si_o3 = DecimalField(
        label='Na₂SiO₃ (m%)',
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

    na2_si_o3_specific = DecimalField(
        label='Na₂SiO₃ specific (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_specific = DecimalField(
        label='NaOH specific (m%)',
        validators=[
            validators.Optional()
        ]
    )

    total = DecimalField(
        label='Total solution (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o = DecimalField(
        label='Na₂O (I) (%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2 = DecimalField(
        label='SiO₂ (I) (%)',
        validators=[
            validators.Optional()
        ]
    )

    h2_o = DecimalField(
        label='H₂O (%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o_dry = DecimalField(
        label='Na₂O (dry) (m%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2_dry = DecimalField(
        label='SiO₂ (dry) (m%)',
        validators=[
            validators.Optional()
        ]
    )

    water = DecimalField(
        label='Water (m%)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_total = DecimalField(
        label='Total NaOH (m%)',
        validators=[
            validators.Optional()
        ]
    )
