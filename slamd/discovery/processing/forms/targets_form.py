from flask_wtf import FlaskForm as Form
from wtforms import SubmitField, StringField, validators, SelectMultipleField


class TargetsForm(Form):

    target_value = StringField(
        label='1. Add new target',
        validators=[validators.DataRequired(message='Name cannot be empty')],
    )

    choose_target_field = SelectMultipleField(
        label='2. Choose existing target for adding labels',
        validators=[validators.DataRequired(message='Target cannot be empty')],
        choices=[]
    )

    submit = SubmitField('3 - Save targets')
