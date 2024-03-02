from flask import session


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session["design_assistant"] = {}

    @classmethod
    def update_session(cls, value, key):
        if key is None and value in ["zero_shot_learner", "data_creation"]:
            session["design_assistant"]["zero_shot_learner"] = {}
        if key is None and value in ["import_data", "None"]:
            session["design_assistant"]["dataset"] = "None"
        if key == "type":
            print("key is not none", key)
            session["design_assistant"]["zero_shot_learner"]["type"] = value
        if key == "design_targets":
            if isinstance(value, dict):
                print("is dict", value)
                design_targets = []
                for k, v in value.items():
                    design_targets.append({k: v})
                session["design_assistant"]["zero_shot_learner"][
                    "design_targets"
                ] = design_targets
            if isinstance(value, list):
                print("is list", value)
                session["design_assistant"]["zero_shot_learner"][
                    "design_targets"
                ] = value
        if key == "powders":
            selected_powders = value["selected_powders"]
            blend_powders = value["blend_powders"]
            session["design_assistant"]["zero_shot_learner"]["powders"] = {
                "selected": selected_powders,
                "blend": blend_powders,
            }
        if key == 'liquid':
            selected_liquid = value
            session["design_assistant"]["zero_shot_learner"]["liquid"] = selected_liquid

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)

    @classmethod
    def delete_session_key(cls, key):
        if key in session.keys():
            session.pop(key)
