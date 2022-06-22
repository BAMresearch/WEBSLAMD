from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, StringField


class AdmixtureForm(Form):

    composition = DecimalField(label='Composition')

    type = StringField(label='Type')
