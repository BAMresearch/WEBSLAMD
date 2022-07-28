from wtforms import DecimalField, validators

from slamd.materials.processing.forms.materials_form import MaterialsForm


class ProcessForm(MaterialsForm):

    duration = DecimalField(
        label='Duration (days)',
        validators=[
            validators.Optional()
        ]
    )

    temperature = DecimalField(
        label='Temperature (°C)',
        validators=[
            validators.Optional()
        ]
    )

    relative_humidity = DecimalField(
        label='Relative Humidity (%)',
        validators=[
            validators.Optional()
        ]
    )
