from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, SelectField, validators
from wtforms import StringField


class MinMaxEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    increment = DecimalField('Increment (Vol.-%)')

    min = DecimalField('Min (Vol.-%)')

    max = DecimalField('Max (Vol.-%)')


class MinMaxForm(Form):

    blending_strategy = SelectField(label='Blending Strategy', choices=['Volume-based', 'Weight-based'])

    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm), min_entries=0)
