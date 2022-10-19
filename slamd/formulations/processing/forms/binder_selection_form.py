from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField, SubmitField, DecimalField, StringField


"""
We explicitly choose to have dedicated forms for different building materials even though the code looks similar.
However, we do not want to create a tight coupling between different usecases which can diverge in the future. Further-
more in case we are adding more and more types of bulding materials, dedicated forms (and corresponding html files)
lead too much more flexibility and extensibility.
"""
class BinderSelectionForm(Form):

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
        label='1.3 - Aggregates (optional)',
        validators=[validators.Optional()],
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
