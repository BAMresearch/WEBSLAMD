from flask_wtf import FlaskForm as Form
from wtforms import StringField


class AddPropertyForm(Form):

    name = StringField(label='Name')
    value = StringField(label='Value')
