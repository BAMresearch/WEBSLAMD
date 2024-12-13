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

    gravity = DecimalField(
        label='Specific gravity',
        validators=[
            validators.Optional()
        ])

    bulk_density = DecimalField(
        label='Bulk density (kg/m³)',
        validators=[
            validators.Optional()
        ])

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
        label='Aggregate density (t/m³)',
        default=2.4,
        validators=[
            validators.Optional()
        ]
    )
