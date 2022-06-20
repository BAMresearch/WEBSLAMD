from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField


class BaseMaterialsForm(Form):

    # TODO: validation -> name must be unique
    material_name = StringField(
        label='Name')

    material_type = SelectField(
        'Type of the Material',
        choices=['Powder', 'Liquid', 'Aggregates', 'Admixture', 'Additive', 'Process', 'Custom']
    )
