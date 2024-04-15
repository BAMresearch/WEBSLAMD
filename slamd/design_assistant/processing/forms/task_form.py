from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms import validators


class TaskForm(Form):
    task_field = RadioField(
        label="Please select:",
        choices=[
            ("data_creation", "🧑‍🚀 Start a new SLAMD Project"),
            ("zero_shot_learner", "🤖 Zero-shot Designs using LLMs"),
        ],
        validators=[validators.DataRequired(message="Service cannot be empty!")],
    )
    # You can add a separate attribute for detailed instructions.
    instructions = ("👋 Welcome to the Design Assistant! I'm here to guide you through "
                    "the process of designing high-quality cementitious materials.\n\n"
                    "We have two options for you to choose from:\n\n"
                    "1. 🧑‍🚀Start a new SLAMD Project \n "
                    "This option helps you to get started with SLAMD. Together, "
                    "we'll set up SLAMD's Digital Lab, compile base materials and processes to create a material formulation data set. "
                    "After we initialized the project you can always refine your creations via the digital lab in the navigation bar.\n\n"
                    "2. 🤖Zero-shot Designs using LLMs \n"
                    " Need quick insights without the hassle of collecting training data? "
                    "Let's jump straight into using language models to output formulations using mankind's collective knowledge. "
                    "I will assist you in crafting a structured prompt to unlock high-performance predictions. Perfect for when time is of the essence! \n\n")