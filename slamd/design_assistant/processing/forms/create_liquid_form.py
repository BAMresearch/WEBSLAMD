from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, validators


class CreateLiquidForm(Form):

    name_field = StringField(label="Great! We continue by creating liquids. What kind of liquid do you want to add?")
