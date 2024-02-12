from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators


class TaskForm(Form):
    task_field = RadioField(
        label="How can I help you Today?",
        choices=[
            "Create a new Data Set in the digital Lab",
            "Zero shot predictions using LLMs",
        ],
        validators=[validators.DataRequired(message="Service cannot be empty!")],
    )
