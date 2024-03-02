from flask_wtf import FlaskForm as Form
from wtforms import (
    RadioField,
    validators,
    DecimalField,
    SubmitField,
    SelectMultipleField,
    widgets,
    FieldList,
    FormField,
    StringField,
)
from wtforms.widgets import ListWidget, CheckboxInput
from slamd.design_assistant.processing.forms.additional_design_target_form import (
    AdditionalDesignTargetForm,
)


class CampaignForm(Form):

    material_type_field = RadioField(
        label="Understood. Let’s design a Material. What do you want to create: a binder or a concrete?",
        choices=["Concrete", "Binder"],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    design_targets_field = SelectMultipleField(
        label="Great! What are the targets of your design? (Click most important targets, add target value optional, select up to two different targets)",
        choices=[
            ("strength", "Strength : "),
            ("workability", "Workability : "),
            ("reactivity", "Reactivity : "),
            ("sustainability", "Sustainability : "),
            ("cost", "Cost : "),
        ],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        validators=[validators.DataRequired(message="Select at least one target!")],
    )

    target_strength_field = DecimalField("Target Value (optional): Min MPa ")

    target_workability_field = DecimalField("Slump (optional): Min mm ")

    target_reactivity_field = DecimalField("Target Value (optional): Min °C ")

    target_sustainability_field = DecimalField("Target Value (optional): Max CO_2/t ")

    target_cost_field = DecimalField("Target Value (optional): Max €/t ")

    additional_design_targets = FieldList(
        FormField(AdditionalDesignTargetForm), min_entries=0, max_entries=10
    )

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
        label="Anything else?",
        choices=[
            ("scm", "SCM"),
            ("super_plasticizer", "Super Plasticizer"),
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    additional_other = StringField()

    submit_button = SubmitField("Save")
