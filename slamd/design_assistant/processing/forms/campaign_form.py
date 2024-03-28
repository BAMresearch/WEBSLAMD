from flask_wtf import FlaskForm as Form
from wtforms import (RadioField, validators, SubmitField, SelectMultipleField, FieldList, FormField, StringField, )
from wtforms.widgets import ListWidget, CheckboxInput

from slamd.design_assistant.processing.forms.design_targets_form import DesignTargetsForm


class CampaignForm(Form):
    material_type_field = RadioField(
        label="Understood. Let’s design a Material. What do you want to create: a binder or a concrete?",
        choices=["Concrete", "Binder"],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    standard_design_targets_field = SelectMultipleField(
        label="Great! What are the targets of your design? (Click most important targets, add target value optional, select up to two different targets)",
        choices=["Strength", "Workability", "Reactivity", "Sustainability", "Cost"],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one target!")],
    )

    design_targets = FieldList(FormField(DesignTargetsForm), min_entries=0, max_entries=2)

    select_powders_field = SelectMultipleField(
        label="Perfect! Let’s move on. What type of powders do you want to use?",
        choices=[
            ("opc", "Add OPC"),
            ("fly_ash", "Fly Ash"),
            ("ggbfs", "GGBFS"),
            ("geopolymer", "Geopolymer"),
        ],
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one powder!")],
    )

    blend_powders_field = RadioField(
        label="Blend powders? (Minimum of two powders need to be selected.)",
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    liquids_field = RadioField(
        label="Great! Let's select the liquid?",
        choices=[
            ("pure_water", "Pure Water"),
            ("activator_liquid", "Activator Liquid (H2O, NaOH, Na2SiO3)"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_liquid = StringField()

    other_field = RadioField(
        label="Anything else? (optional)",
        choices=[
            ("scm", "SCM"),
            ("super_plasticizer", "Super Plasticizer"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_other = StringField()

    comment_field = StringField(label="Ok! Is there anything else you want me to know? (optional)")

    design_knowledge_field = StringField(
        label="Design knowledge",
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    formulation_field = StringField(label="Okay, based on all the information your provided me with, the following is my suggestion for a formulation: ")

    submit_button = SubmitField("Save")
