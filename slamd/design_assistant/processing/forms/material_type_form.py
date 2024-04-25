from flask_wtf import FlaskForm as Form
from wtforms import RadioField, validators


class MaterialTypeForm(Form):

    init_intro_text = "I will guide you through the process of framing your design problem as a structured prompt for the LLM."
    init_process_overview = "Here's how we'll proceed:"
    init_step_one = "Our goal is to guide the LLM output to meet the rules and standards relevant to your project."
    init_step_two = "First, we will explore your design problem and gather all the key requirements."
    init_step_three = "Later, you will have the opportunity to provide detailed context, such as the objectives of your project and the specific conditions that need to be considered."

    material_type_field = RadioField(
        label="Let's start with a basic question: What type of material are we working on?",
        choices=[("Concrete", "Concrete Formulation"), ("Binder", "Binder Formulation")],
        validators=[validators.DataRequired(message="Please make a selection!")],
    )