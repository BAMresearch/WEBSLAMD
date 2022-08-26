from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, BooleanField, SelectField, StringField


class MaterialsAndProcessesSelectionForm(Form):

    powder_selection = SelectMultipleField(
        label='1.1 - Powders',
        validators=[validators.DataRequired()],
        choices=[]
    )

    liquid_selection = SelectMultipleField(
        label='1.2 - Liquids',
        validators=[validators.DataRequired()],
        choices=[]
    )

    aggregates_selection = SelectMultipleField(
        label='1.3 - Aggregates',
        validators=[validators.DataRequired()],
        choices=[]
    )

    admixture_selection = SelectMultipleField(
        label='1.4 - Admixture',
        validators=[validators.DataRequired()],
        choices=[]
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

    weight_constraint = DecimalField(
        label='1.7 - Constraint (Sum of materials used for formulation) (kg)'
    )

    submit = SubmitField(label='7 - Submit Dataset')
