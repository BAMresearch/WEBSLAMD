from slamd.design_assistant.processing.design_assistant_factory import (
    DesignAssistantFactory,
)
from slamd.design_assistant.processing.design_assistant_persistence import (
    DesignAssistantPersistence,
)
from flask import session


class DesignAssistantService:

    @classmethod
    def create_design_assistant_form(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property(
            "design_assistant"
        )
        form = DesignAssistantFactory.create_design_assistant_form()
        if not design_assistant_session:
            cls.init_design_assistant_session()
            form.import_form = None
            form.campaign_form = None
        if design_assistant_session:
            form.task_form.task_field.data = list(design_assistant_session.keys())[0]
            if "dataset" in list(design_assistant_session.keys()):
                form.import_form.import_selection_field.data = design_assistant_session[
                    "dataset"
                ]
                if "zero_shot_learner" in list(design_assistant_session.keys()):
                    print(design_assistant_session["zero_shot_learner"].keys())
                    for key, value in design_assistant_session[
                        "zero_shot_learner"
                    ].items():
                        print(key)
                        if key == "type":
                            form.campaign_form.material_type_field.data = value
            else:
                form.campaign_form = None
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantFactory.create_design_assistant_task_form()
        return form

    @classmethod
    def create_design_assistant_import_selection_form(cls):
        form = DesignAssistantFactory.create_design_assistant_import_selection_form()
        return form

    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = DesignAssistantFactory.create_design_assistant_campaign_form()
        return form

    @classmethod
    def init_design_assistant_session(cls):
        DesignAssistantPersistence.init_session()

    @classmethod
    def update_design_assistant_session(cls, value, key=None):
        DesignAssistantPersistence.update_session(value, key)

    @classmethod
    def populate_form(cls):
        pass
