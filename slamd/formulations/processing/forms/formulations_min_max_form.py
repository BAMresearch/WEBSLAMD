from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, DecimalField, StringField, validators


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


class NonEditableFormulationItemsForm(Form):
    uuid_field = StringField(label='UUID')

    type_field = StringField(
        validators=[validators.DataRequired(message='Type cannot be empty')]
    )

    materials_entry_name = StringField(
        validators=[validators.DataRequired(message='Entry name cannot be empty')]
    )


class FormulationsMinMaxForm(Form):

    materials_min_max_entries = FieldList(FormField(MaterialsMinMaxEntriesForm), min_entries=0)

    process_entries = FieldList(FormField(NonEditableFormulationItemsForm), min_entries=0)

    liquid_info_entry = StringField(
        validators=[validators.DataRequired(message='Entry name cannot be empty')]
    )
