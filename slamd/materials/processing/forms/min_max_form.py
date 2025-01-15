from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, validators
from wtforms import StringField


class MinMaxEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    increment = DecimalField('Increment (%)')

    min = DecimalField('Min (%)')

    max = DecimalField('Max (%)')


class MinMaxForm(Form):

    total_volume = DecimalField(
        label='Total Volume (m³)',
        default=1,
        validators=[validators.DataRequired(message='Total volume cannot be empty')]
    )

    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm), min_entries=0)
