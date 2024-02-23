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
        if key is not None:
            session["design_assistant"]["zero_shot_learner"][key] = value
        if isinstance(value, dict):
            design_targets = []
            for k, v in value.items():
                design_targets.append({k: v})
            session["design_assistant"]["zero_shot_learner"][
                "design_targets"
            ] = design_targets
        if isinstance(value, list):
            session["design_assistant"]["zero_shot_learner"]["design_targets"] = value

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)
