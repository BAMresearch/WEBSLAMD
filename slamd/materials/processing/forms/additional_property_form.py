from flask_wtf import FlaskForm as Form
from wtforms import StringField


class AdditionalPropertyForm(Form):

    property_name = StringField(label='Name')
    property_value = StringField(label='Value')
