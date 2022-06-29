from wtforms import DecimalField, StringField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class AggregatesForm(BaseMaterialsForm):

    fine_aggregates = DecimalField(label='Fine Aggregates')

    coarse_aggregates = DecimalField(label='Coarse Aggregates')

    fa_density = StringField(label='FA Density')

    ca_density = StringField(label='CA Density')
