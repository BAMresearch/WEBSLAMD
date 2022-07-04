from wtforms import DecimalField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class PowderForm(BaseMaterialsForm):

    fe3_o2 = DecimalField(
        label='Fe2O3 (m%)',
        validators=[
            validators.Optional()
        ]
    )

    si_o2 = DecimalField(
        label='SiO2 (m%)',
        validators=[
            validators.Optional()
        ]
    )

    al2_o3 = DecimalField(
        label='Al2O3 (m%)',
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
        label='Na2O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    k2_o = DecimalField(
        label='K2O (m%)',
        validators=[
            validators.Optional()
        ]
    )

    s_o3 = DecimalField(
        label='SO3 (m%)',
        validators=[
            validators.Optional()
        ]
    )

    ti_o2 = DecimalField(
        label='TiO2 (m%)',
        validators=[
            validators.Optional()
        ]
    )

    p2_o5 = DecimalField(
        label='P2O5 (m%)',
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
        label='Mn2O3 (m%)',
        validators=[
            validators.Optional()
        ]
    )

    fine = DecimalField(
        label='Fine modules (m2/kg)',
        validators=[
            validators.Optional()
        ]
    )

    gravity = DecimalField(
        label='Specific gravity (m%)',
        validators=[
            validators.Optional()
        ]
    )
