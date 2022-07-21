from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, validators
from wtforms import StringField


class FormulationsMinMaxEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    formulations_entry_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    increment = DecimalField('Increment (kg)')

    min = DecimalField('Min (kg)')

    max = DecimalField('Max (kg)')


class FormulationsMinMaxForm(Form):
    all_formulations_min_max_entries = FieldList(FormField(FormulationsMinMaxEntriesForm), min_entries=0)
