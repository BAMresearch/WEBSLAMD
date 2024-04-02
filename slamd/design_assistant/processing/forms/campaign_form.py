from flask_wtf import FlaskForm as Form
from wtforms import (RadioField, validators, SubmitField, SelectMultipleField, FieldList, FormField, StringField, )
from wtforms.widgets import ListWidget, CheckboxInput

from slamd.design_assistant.processing.forms.design_targets_form import DesignTargetsForm


class CampaignForm(Form):
    # Breaking down the guidance into separate attributes
    init_intro_text = "I will guide you through the process of framing your design problem as a structured prompt for the LLM."
    init_process_overview = "Here's how we'll proceed:"
    init_step_one = "Our goal is to guide the LLM output to meet the rules and standards relevant to your project."
    init_step_two = "First, we will explore your design problem and gather all the key requirements."
    init_step_three = "Later, you will have the opportunity to provide detailed context, such as the objectives of your project and the specific conditions that need to be considered."

    targ_intro_text = "Let's define the objectives of your design to align the LLM's outputs with your specific needs."
    targ_process_overview = "Please keep in mind:"
    targ_step_one = "Your choices here will steer the direction of our upcoming steps in formulating the ideal mix design."
    targ_step_two = "You are encouraged to select up to two primary objectives"
    targ_step_three = "For each selected objective, you'll have the opportunity to specify target values in the subsequent step."

    material_type_field = RadioField(
        label="Let's start with a basic question: What type of material are we working on?",
        choices=[("Concrete", "Concrete Formulation"), ("Binder","Binder Formulation")],
        validators=[validators.DataRequired(message="Please make a selection!")],
    )

    standard_design_targets_field = SelectMultipleField(
        label="What are the most important design targets?",
        choices=[("Strenght", "Compressive Strength"), ("Workability", "Workability"), ("CarbonationResistance", "Carbonation Resistance"), ("Costs", "Costs")],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one target!")],
    )
    design_targets = FieldList(FormField(DesignTargetsForm), min_entries=0, max_entries=2)

    select_powders_field = SelectMultipleField(
        label="Great! Now, let's select the types of powders for your mix. Please choose from the following options:",
        choices=[
            ("opc", "OPC (Ordinary Portland Cement)"),
            ("fly_ash", "Fly Ash"),
            ("ggbfs", "GGBFS (Ground Granulated Blast Furnace Slag)"),
            ("geopolymer", "Geopolymer (e.g. industrial byproducts)"),
        ],
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one powder!")],
    )

    blend_powders_field = RadioField(
        label="Do you want to blend powders? Note: Blending requires selecting a minimum of two powders.",
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    liquids_field = RadioField(
        label="Now, select your mixing liquid:",
        choices=[
            ("water", "Water"),
            ("activator_liquid", "Activator Solution (Triggers the chemical reaction in geopolymer concrete, using water mixed with sodium hydroxide and sodium silicate)"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_liquid = StringField()

    other_field = RadioField(
        label="Anything else? (optional)",
        choices=[
            ("biochar", "Biochar"),
            ("rice_husk_ash", "Rice Husk Ash"),
            ("recycled_aggregates", "Recycled Aggregates"),
            ("limestone", "Limestone Powder"),
            ("recycled_glass_fines", "Recycled Glass Fines"),
            ("super_plasticizer", "Super Plasticizer"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_other = StringField()

    comment_field = StringField(label="Great! To ensure we tailor the mix design perfectly to your needs, is there any additional information or specific requirements you'd like to share? For example, resource availability, important boundary conditions, desired performance characteristics, sustainability goals, or any other details that may influence the mix design. Feel free to provide as much detail as you'd like!")

    design_knowledge_field = StringField(
        label="Design knowledge",
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    submit_button = SubmitField("Submit")
