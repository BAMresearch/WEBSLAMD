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

    increment = DecimalField('Increment (for Powders/Aggregates: kg, for Liquids: w/z ratio)')

    min = DecimalField('Min (for Powders/Aggregates: kg, for Liquids: w/z ratio)')

    max = DecimalField('Max (for Powders/Aggregates: kg, for Liquids: w/z ratio)')


class NonEditableFormulationItemsForm(Form):

    uuid_field = StringField(label='UUID')

    type_field = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )

    materials_entry_name = StringField(
        label='Name',
        validators=[validators.DataRequired(message='Name cannot be empty')]
    )


class FormulationsMinMaxForm(Form):

    materials_min_max_entries = FieldList(FormField(MaterialsMinMaxEntriesForm), min_entries=0)
    non_editable_entries = FieldList(FormField(NonEditableFormulationItemsForm), min_entries=0)
