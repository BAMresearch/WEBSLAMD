from flask_wtf import FlaskForm as Form
from wtforms import DecimalField


class PowderForm(Form):
    feo = DecimalField(
        label='Fe2O3 (%m)'
    )
    sio = DecimalField(
        label='SiO2 (%m)'
    )
    alo = DecimalField(
        label='Al2O3 (%m)'
    )
    cao = DecimalField(
        label='CaO (%m)'
    )
    mgo = DecimalField(
        label='MgO (%m)'
    )
    nao = DecimalField(
        label='Na2O (%m)'
    )
    ko = DecimalField(
        label='K2O (%m)'
    )
    so = DecimalField(
        label='SO3 (%m)'
    )
    tio = DecimalField(
        label='TiO2 (%m)'
    )
    po = DecimalField(
        label='P2O5 (%m)'
    )
    sro = DecimalField(
        label='SrO (%m)'
    )
    mno = DecimalField(
        label='Mn2O3 (%m)'
    )
    fine = DecimalField(
        label='Fine modules (m2/kg)'
    )
    gravity = DecimalField(
        label='Specific gravity (%m)'
    )
