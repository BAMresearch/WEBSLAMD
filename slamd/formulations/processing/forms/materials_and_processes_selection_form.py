from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, BooleanField, SelectField, StringField


class MaterialsAndProcessesSelectionForm(Form):

    powder_selection = SelectMultipleField(
        label='1.1 - Powders (select one at least)',
        validators=[validators.DataRequired(message='Select at least one powder')],
        choices=[]
    )

    liquid_selection = SelectMultipleField(
        label='1.2 - Liquids (select one at least)',
        validators=[validators.DataRequired(message='Select at least one liquid')],
        choices=[]
    )

    aggregates_selection = SelectMultipleField(
        label='1.3 - Aggregates (select one at least)',
        validators=[validators.DataRequired(message='Select at least one aggregate')],
        choices=[]
    )

    admixture_selection = SelectMultipleField(
        label='1.4 - Admixture (optional)',
        validators=[validators.Optional()],
        choices=[]
    )

    custom_selection = SelectMultipleField(
        label='1.5 - Custom (optional)',
        validators=[validators.Optional()],
        choices=[]
    )

    process_selection = SelectMultipleField(
        label='1.6 - Processes (optional)',
        validators=[validators.Optional()],
        choices=[]
    )

    weight_constraint = DecimalField(
        label='1.7 - Constraint (Sum of materials used for formulation) (kg) *',
        validators=[validators.DataRequired(message='Weight constraint cannot be empty')]
    )

    dataset_name = StringField(
        label='1.8 - Name of the dataset (optional)',
        validators=[validators.DataRequired(message='Dataset name cannot be empty')]
    )

    submit = SubmitField(label='Submit')
