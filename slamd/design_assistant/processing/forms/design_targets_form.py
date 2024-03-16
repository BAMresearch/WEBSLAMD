from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, RadioField


class DesignTargetsForm(Form):

    design_target_name_field = StringField(label="Design Target Name")

    design_target_value_field = DecimalField(label="Design Target Value")

    design_target_optimization_field = RadioField(choices=[('maximize', 'Maximize target value'),
                                                     ('minimize','Minimize target value')])
