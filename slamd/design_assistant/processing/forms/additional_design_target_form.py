from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField


class AdditionalDesignTargetForm(Form):

    design_target_name = StringField(label="Name")

    design_target_value = DecimalField(label="Target Value")
