from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField
from wtforms import StringField


class MinMaxEntriesForm(Form):
    name = StringField('Name')
    increment = DecimalField('Increment (%)')
    min = DecimalField('Min (%)')
    max = DecimalField('Max (%)')


class MinMaxForm(Form):
    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm), min_entries=0)
