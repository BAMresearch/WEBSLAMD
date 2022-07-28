from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, validators, BooleanField
from wtforms import StringField


class MaterialsMinMaxEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    type_field = StringField(label='Material Type')

    materials_entry_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    increment = DecimalField('Increment (kg)')

    min = DecimalField('Min (kg)')

    max = DecimalField('Max (kg)')


class ProcessesEntriesForm(Form):

    uuid_field = StringField(label='UUID')

    process_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )


class FormulationsMinMaxForm(Form):

    materials_min_max_entries = FieldList(FormField(MaterialsMinMaxEntriesForm), min_entries=0)
    processes_entries = FieldList(FormField(ProcessesEntriesForm), min_entries=0)
