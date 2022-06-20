from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField


class AddPropertyForm(Form):

    name = StringField(label='Name')
    value = StringField(label='Value')

    add_button = SubmitField('Add')
