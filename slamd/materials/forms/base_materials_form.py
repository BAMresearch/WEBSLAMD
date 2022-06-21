from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SubmitField, validators


class BaseMaterialsForm(Form):

    # TODO: validation -> name must be unique
    material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message="Material name cannot be empty")]
    )

    material_type = SelectField(
        label='Material type',
        validators=[validators.DataRequired()],
        choices=['Powder', 'Liquid', 'Aggregates',
                 'Admixture', 'Additive', 'Process', 'Custom']
    )

    submit = SubmitField('Add material')
