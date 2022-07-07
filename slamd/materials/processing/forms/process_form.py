from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class ProcessForm(MaterialsForm):

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
