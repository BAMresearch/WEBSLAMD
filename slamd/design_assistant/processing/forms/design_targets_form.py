from flask_wtf import FlaskForm as Form
from wtforms import StringField, RadioField


class DesignTargetsForm(Form):
    design_target_name_field = StringField(label="Design Target Name")

    design_target_value_field = StringField(label="Enter the target value bound and its unit")

    design_target_optimization_field = RadioField(label='Should the target value be maximized or minimized?',
                                                  choices=[('increase', 'Increase'), ('decrease', 'Decrease')])
