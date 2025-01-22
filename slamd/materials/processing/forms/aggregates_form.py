from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class AggregatesForm(MaterialsForm):
    fine_aggregates = DecimalField(
        label='Fine Aggregates (m%)',
        validators=[
            validators.Optional()
        ]
    )

    coarse_aggregates = DecimalField(
        label='Coarse Aggregates (m%)',
        validators=[
            validators.Optional()
        ]
    )

    fineness_modulus = DecimalField(
        label='Fineness modulus (m³/kg)',
        validators=[
            validators.Optional()
        ])

    water_absorption = DecimalField(
        label='Water absorption (m%)',
        validators=[
            validators.Optional()
        ])

    density = DecimalField(
        label='Aggregates Specific Gravity',
        default=2.65,
        validators=[
            validators.DataRequired(message='Material density cannot be empty')
        ]
    )
