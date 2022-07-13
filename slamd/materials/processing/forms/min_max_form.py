from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, validators
from wtforms import StringField


class MinMaxEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    increment = DecimalField(
        'Increment (%)',
        validators=[validators.NumberRange(min=0, max=100, message='Increment must be a number between 0 and 100')])

    min = DecimalField(
        'Min (%)',
        validators=[validators.NumberRange(min=0, max=100, message='Min must be a number between 0 and 100')])

    max = DecimalField(
        'Max (%)',
        validators=[validators.NumberRange(min=0, max=100, message='Max must be a number between 0 and 100')])


class MinMaxForm(Form):
    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm), min_entries=0)
