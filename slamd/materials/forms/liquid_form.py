from flask_wtf import FlaskForm as Form
from wtforms import DecimalField


class LiquidForm(Form):

    precursor = DecimalField(label='Precursor')
