from wtforms import DecimalField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class PowderForm(BaseMaterialsForm):

    feo = DecimalField(
        label='Fe2O3 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    sio = DecimalField(
        label='SiO2 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    alo = DecimalField(
        label='Al2O3 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    cao = DecimalField(
        label='CaO (%m)',
        validators=[
            validators.Optional()
        ]
    )
    mgo = DecimalField(
        label='MgO (%m)',
        validators=[
            validators.Optional()
        ]
    )

    nao = DecimalField(
        label='Na2O (%m)',
        validators=[
            validators.Optional()
        ]
    )
    ko = DecimalField(
        label='K2O (%m)',
        validators=[
            validators.Optional()
        ]
    )

    so = DecimalField(
        label='SO3 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    tio = DecimalField(
        label='TiO2 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    po = DecimalField(
        label='P2O5 (%m)',
        validators=[
            validators.Optional()
        ]
    )

    sro = DecimalField(
        label='SrO (%m)',
        validators=[
            validators.Optional()
        ]
    )

    mno = DecimalField(
        label='Mn2O3 (%m)',
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
        label='Specific gravity (%m)',
        validators=[
            validators.Optional()
        ]
    )
