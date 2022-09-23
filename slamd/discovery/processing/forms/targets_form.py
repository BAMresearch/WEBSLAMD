from flask_wtf import FlaskForm as Form
from wtforms import SubmitField, StringField, validators, SelectMultipleField


class TargetsForm(Form):

    target_value = StringField(
        label='1.1 Either add a new target column...',
        validators=[validators.DataRequired(message='Name cannot be empty')],
    )

    choose_target_field = SelectMultipleField(
        label='1.2 ...or choose an existing column to edit',
        validators=[validators.DataRequired(message='Target cannot be empty')],
        choices=[]
    )

    submit = SubmitField('3 - Save targets')
