from flask_wtf import FlaskForm as Form
from wtforms import (RadioField, validators, SubmitField, SelectMultipleField, FieldList, FormField, StringField, )
from wtforms.widgets import ListWidget, CheckboxInput

from slamd.design_assistant.processing.forms.design_targets_form import DesignTargetsForm


class CampaignForm(Form):
    # Breaking down the guidance into separate attributes


    targ_intro_text = "Let's define the objectives of your design to align the LLM's outputs with your specific needs."
    targ_process_overview = "Please keep in mind:"
    targ_step_one = "Your choices here will steer the direction of our upcoming steps in formulating the ideal mix design."
    targ_step_two = "You are encouraged to select up to two primary objectives"
    targ_step_three = "For each selected objective, you'll have the opportunity to specify target values in the subsequent step."

    standard_design_targets_field = SelectMultipleField(
        label="What are the most important design targets?",
        choices=["Compressive Strength", "Workability", "Carbonation Resistance", "Costs"],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one target!")],
    )

    design_targets = FieldList(FormField(DesignTargetsForm), min_entries=0, max_entries=2)

    select_powders_field = SelectMultipleField(
        label="Great! Now, let's select the types of powders for your mix. Please choose from the following options:",
        choices=[
            ("OPC", "OPC (Ordinary Portland Cement)"), ("Fly Ash", "Fly Ash"),
            ("GGBFS", "GGBFS (Ground Granulated Blast Furnace Slag)"),
            ("Geopolymer", "Geopolymer (e.g. industrial byproducts)"),
        ],
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one powder!")],
    )

    blend_powders_field = RadioField(
        label="Do you want to blend powders? Note: Blending requires selecting a minimum of two powders.",
        choices=["Yes","No"],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    liquids_field = SelectMultipleField(
        label="Now, select your mixing liquid:",
        choices=[("Water", "Water"), ("Activator Liquid", "Activator Liquid")],
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_liquid = StringField()

    other_field = SelectMultipleField(
        label="Anything else? (optional)",
        choices=["Biochar", "Rice Husk Ash", "Recycled Aggregates" , "Limestone Powder", "Recycled Glass Fines", "Super Plasticizer"],
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_other = StringField()

    comment_field = StringField(
        label="Great! To ensure we tailor the mix design perfectly to your needs, is there any additional information or specific requirements you'd like to share? For example, resource availability, important boundary conditions, desired performance characteristics, sustainability goals, or any other details that may influence the mix design. Feel free to provide as much detail as you'd like!")

    design_knowledge_field = StringField(
        label="Design knowledge",
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    formulation_field = StringField(label="Okay, based on all the information your provided me with, the following is my suggestion for a formulation: ")

    submit_button = SubmitField("Submit")
