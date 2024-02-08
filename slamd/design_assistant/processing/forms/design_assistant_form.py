from flask_wtf import FlaskForm as Form
from wtforms import SubmitField

class DesignAssistantForm(Form):
    submit = SubmitField('Submit')
    