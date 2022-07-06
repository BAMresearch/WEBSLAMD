from wtforms import DecimalField, StringField, validators

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class AggregatesForm(BaseMaterialsForm):

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

    fa_density = StringField(label='FA Density')

    ca_density = StringField(label='CA Density')
