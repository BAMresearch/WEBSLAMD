from wtforms import DecimalField, validators

from slamd.materials.processing.forms.base_materials_form import BaseMaterialsForm


class ProcessForm(BaseMaterialsForm):

    duration = DecimalField(
        label='Duration',
        validators=[
            validators.Optional()
        ]
    )

    temperature = DecimalField(
        label='Temperature',
        validators=[
            validators.Optional()
        ]
    )

    relative_humidity = DecimalField(
        label='Relative Humidity',
        validators=[
            validators.Optional()
        ]
    )
