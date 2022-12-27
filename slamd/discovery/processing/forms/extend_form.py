from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ExtendForm(FlaskForm):
    min_value = IntegerField('Minimum value', validators=[DataRequired(), NumberRange(min=0)])
    max_value = IntegerField('Maximum value', validators=[DataRequired(), NumberRange(min=0)])
    string_columns = SelectMultipleField('Select the String columns',
                                         choices=[('col1', 'Column 1'), ('col2', 'Column 2'), ('col3', 'Column 3')])
    target_columns = SelectMultipleField('Select the target columns',
                                         choices=[('col1', 'Column 1'), ('col2', 'Column 2'), ('col3', 'Column 3')])
    num_samples = IntegerField('Number of samples', validators=[DataRequired(), NumberRange(min=1)])

    submit = SubmitField('Resample')
