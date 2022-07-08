from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, validators
from wtforms import StringField


class MinMaxEntriesForm(Form):
    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )
    increment = DecimalField('Increment (%)')
    min = DecimalField('Min (%)')
    max = DecimalField('Max (%)')


class MinMaxForm(Form):
    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm), min_entries=0)
