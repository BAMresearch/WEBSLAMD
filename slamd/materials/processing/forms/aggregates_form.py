from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm
from slamd.materials.processing.constants.material_constants import AGGREGATE_DEFAULT_SPECIFIC_GRAVITY

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

    specific_gravity = DecimalField(
        label='Specific Gravity',
        default=AGGREGATE_DEFAULT_SPECIFIC_GRAVITY,
        validators=[
            validators.DataRequired(message='Material specific gravity cannot be empty')
        ]
    )
