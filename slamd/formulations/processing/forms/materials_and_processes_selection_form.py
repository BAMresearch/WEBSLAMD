from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, BooleanField, SelectField, StringField


class MaterialsAndProcessesSelectionForm(Form):
    powder_selection = SelectField(
        label='Powders',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    liquid_selection = SelectField(
        label='Liquids',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    aggregates_selection = SelectField(
        label='Aggregates',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    admixture_selection = SelectField(
        label='Admixture',
        validators=[validators.DataRequired()],
        choices=[('', '')]
    )

    custom_selection = SelectMultipleField(
        label='Custom',
        validators=[validators.DataRequired()],
        choices=[]
    )

    process_selection = SelectMultipleField(
        label='Processes',
        validators=[validators.DataRequired()],
        choices=[]
    )

    targets_field = StringField(
        'Targets (Specify various target values. Follow the pattern "target 1; target 2; target 3".)')

    with_constraint = BooleanField(label='Do you want to set a weight constraint for formulations?')

    weigth_constraint = DecimalField('Constraint (Sum of materials used for formulation) (kg)')

    submit = SubmitField('Create materials formulations')
