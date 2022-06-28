from wtforms import DecimalField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class LiquidForm(BaseMaterialsForm):
    nasio = DecimalField(
        label='Na2SiO3 (%m)'
    )
    naoh = DecimalField(
        label='NaOH (%m)'
    )
    nasio_specific = DecimalField(
        label='Na2SiO3 specific (%m)'
    )
    naoh_specific = DecimalField(
        label='NaOH specific (%m)'
    )
    total = DecimalField(
        label='Total solution (%m)'
    )
    nao = DecimalField(
        label='Na2O (I) (%)'
    )
    sio = DecimalField(
        label='SiO2 (I) (%)'
    )
    ho = DecimalField(
        label='H2O (%)'
    )
    nao_dry = DecimalField(
        label='Na2O (dry) (%m)'
    )
    sio_dry = DecimalField(
        label='SiO2 (dry) (%m)'
    )
    water = DecimalField(
        label='Water (%m)'
    )
    naoh_total = DecimalField(
        label='Total NaOH (%m)'
    )
