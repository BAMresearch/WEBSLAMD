from wtforms import DecimalField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class LiquidForm(BaseMaterialsForm):
    na2_si_o3 = DecimalField(
        label='Na2SiO3 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h = DecimalField(
        label='NaOH (%m)',
        validators=[
            validators.Optional()
        ]
    )

    na2_si_o3_specific = DecimalField(
        label='Na2SiO3 specific (%m)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_specific = DecimalField(
        label='NaOH specific (%m)',
        validators=[
            validators.Optional()
        ]
    )

    total = DecimalField(
        label='Total solution (%m)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o = DecimalField(
        label='Na2O (I) (%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2 = DecimalField(
        label='SiO2 (I) (%)',
        validators=[
            validators.Optional()
        ]
    )

    h2_o = DecimalField(
        label='H2O (%)',
        validators=[
            validators.Optional()
        ]
    )

    na2_o_dry = DecimalField(
        label='Na2O (dry) (%m)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2_dry = DecimalField(
        label='SiO2 (dry) (%m)',
        validators=[
            validators.Optional()
        ]
    )

    water = DecimalField(
        label='Water (%m)',
        validators=[
            validators.Optional()
        ]
    )

    na_o_h_total = DecimalField(
        label='Total NaOH (%m)',
        validators=[
            validators.Optional()
        ]
    )
