from wtforms import DecimalField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class LiquidForm(BaseMaterialsForm):
    na2_si_o3 = DecimalField(
        label='Na2SiO3 (%m)'
    )

    na_o_h = DecimalField(
        label='NaOH (%m)'
    )

    na2_si_o3_specific = DecimalField(
        label='Na2SiO3 specific (%m)'
    )

    na_o_h_specific = DecimalField(
        label='NaOH specific (%m)'
    )

    total = DecimalField(
        label='Total solution (%m)'
    )

    na2_o = DecimalField(
        label='Na2O (I) (%)'
    )

    si_o2 = DecimalField(
        label='SiO2 (I) (%)'
    )

    h2_o = DecimalField(
        label='H2O (%)'
    )

    na2_o_dry = DecimalField(
        label='Na2O (dry) (%m)'
    )

    si_o2_dry = DecimalField(
        label='SiO2 (dry) (%m)'
    )

    water = DecimalField(
        label='Water (%m)'
    )

    na_o_h_total = DecimalField(
        label='Total NaOH (%m)'
    )
