from flask_wtf import FlaskForm as Form
from wtforms import DecimalField


class PowderForm(Form):

    ingredient = DecimalField(label='FeO')
