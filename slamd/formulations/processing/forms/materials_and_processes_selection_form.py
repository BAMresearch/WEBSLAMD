from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, BooleanField


class MaterialsAndProcessesSelectionForm(Form):

    material_selection = SelectMultipleField(
        label='Materials',
        validators=[validators.DataRequired()],
        choices=[]
    )

    process_selection = SelectMultipleField(
        label='Processes',
        validators=[validators.DataRequired()],
        choices=[]
    )

    with_constraint = BooleanField(label='Do you want to set a weight constraint for formulations?')

    weigth_constraint = DecimalField('Constraint (Sum of materials used for formulation) (kg)')

    submit = SubmitField('Create materials formulations')
