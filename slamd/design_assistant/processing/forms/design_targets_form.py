from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, RadioField


class DesignTargetsForm(Form):

    design_target_name_field = StringField(label="Design Target Name")

    design_target_value_field = DecimalField(label="Enter the target value")

    design_target_unit_field = StringField(label="Enter the unit of the target value")

    design_target_bound_field = RadioField(label='Should the target value be the maximum or minimum?',choices=[('maximum', 'Maximum'),('minimum','Minimum')])
