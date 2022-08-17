from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, BooleanField, SelectField, StringField


class MaterialsAndProcessesSelectionForm(Form):
    powder_selection = SelectField(
        label='1.1 - Powders',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    liquid_selection = SelectField(
        label='1.2 - Liquids',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    aggregates_selection = SelectField(
        label='1.3 - Aggregates',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    admixture_selection = SelectField(
        label='1.4 - Admixture',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    custom_selection = SelectMultipleField(
        label='1.5 - Custom',
        validators=[validators.DataRequired()],
        choices=[]
    )

    process_selection = SelectMultipleField(
        label='1.6 - Processes',
        validators=[validators.DataRequired()],
        choices=[]
    )

    targets_field = StringField(
        label='3 - Targets (Specify various target values. Follow the pattern "target 1; target 2; target 3".)'
    )

    with_constraint = BooleanField(
        label='2 - Do you want to set a weight constraint for formulations?'
    )

    weigth_constraint = DecimalField(
        label='Constraint (Sum of materials used for formulation) (kg)'
    )

    submit = SubmitField(label='7 - Create materials formulations')
