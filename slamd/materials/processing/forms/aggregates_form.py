from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class AggregatesForm(MaterialsForm):

    fine_aggregates = DecimalField(
        label='Fine Aggregates',
        validators=[
            validators.Optional()
        ]
    )

    coarse_aggregates = DecimalField(
        label='Coarse Aggregates',
        validators=[
            validators.Optional()
        ]
    )

    fa_density = DecimalField(
        label='FA Density',
        validators=[
            validators.Optional()
        ]
    )

    ca_density = DecimalField(
        label='CA Density',
        validators=[
            validators.Optional()
        ]
    )
