from flask_wtf import FlaskForm as Form
from wtforms import SubmitField


class TargetsForm(Form):
    submit = SubmitField('3 - Save targets')
