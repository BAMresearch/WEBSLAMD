from flask_wtf import FlaskForm as Form
from wtforms import RadioField, FieldList, validators, DecimalField


class DesignAssistantCampaignForm(Form):
    # design_assistant_campaign = FieldList(
    #     DesignAssistantTaskForm, DesignAssistantSelectImportForm
    # )
    material_type = RadioField(
        label="Understood. Let’s design a Material. What do you want to create: a binder or a concrete?",
        choices=[
            "Concrete",
            "Binder",
        ],
        validators=[validators.DataRequired(message="Selection cannot be empty!")],
    )

    design_target = RadioField(
        label="Great! What are the targets of your design?",
        choices=[
            "Strength",
            "Workability",
            "Reactivity",
            "Sustainabilitiy",
            "Cost",
            "+ other",
        ],
    )

    target_strength = DecimalField("Min MPa")

    target_workability = DecimalField("Min mm")

    target_reactivity = DecimalField("Min °C")

    target_sustainability = DecimalField("Max CO_2/t")

    target_cost = DecimalField("Max €/t")
