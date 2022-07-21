from flask_wtf import FlaskForm as Form
from wtforms import StringField, validators, SubmitField, SelectField


class BlendingNameAndTypeForm(Form):
    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired()]
    )

    base_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Custom']
    )

    submit = SubmitField('Create blended materials')
