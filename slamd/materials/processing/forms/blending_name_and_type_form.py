from flask_wtf import FlaskForm as Form
from wtforms import StringField, validators, SubmitField, SelectField


class BlendingNameAndTypeForm(Form):
    blended_material_name = StringField(
        label='1 - Name *',
        validators=[validators.DataRequired(message='Blended material name cannot be empty')]
    )

    base_type = SelectField(
        label='2 - Material type *',
        validators=[validators.DataRequired(message='Base material type cannot be empty')],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Custom']
    )

    submit = SubmitField('Submit')
