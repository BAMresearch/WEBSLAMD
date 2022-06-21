from flask_wtf import FlaskForm as Form
from wtforms import DecimalField


class ProcessForm(Form):

    duration = DecimalField(label='Duration')

    temperature = DecimalField(label='Temperature')

    relative_humidity = DecimalField(label='Relative Humidity')
