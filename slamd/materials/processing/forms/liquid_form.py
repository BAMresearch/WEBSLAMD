from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


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
