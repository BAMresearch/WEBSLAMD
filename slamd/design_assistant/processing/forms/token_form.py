from flask_wtf import FlaskForm as Form
from wtforms.fields.simple import PasswordField


class TokenForm(Form):

    token = PasswordField(label='Insert you Open AI API Key here')
