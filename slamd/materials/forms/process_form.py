from flask_wtf import FlaskForm as Form
from wtforms import DecimalField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class ProcessForm(BaseMaterialsForm):

    duration = DecimalField(label='Duration')

    temperature = DecimalField(label='Temperature')

    relative_humidity = DecimalField(label='Relative Humidity')
