from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SubmitField, validators


class BaseMaterialsForm(Form):

    # TODO: validation -> name must be unique
    material_name = StringField(
        label='Name',
        validators=[validators.DataRequired()]
    )

    material_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Additive', 'Process', 'Custom']
    )

    material_unit = SelectField(
        label='Unit',
        validators=[validators.DataRequired()],
        choices=["Liter", "Kilogram"]
    )
