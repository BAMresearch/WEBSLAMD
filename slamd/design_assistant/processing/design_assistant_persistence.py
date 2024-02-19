from flask import session


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session["design_assistant"] = {}

    @classmethod
    def update_session(cls, value, key):
        # print(value)
        print(key)
        if key is None and value in ["zero_shot_learner", "data_creation"]:
            session["design_assistant"]["zero_shot_learner"] = {}
        if key is None and value in ["no_import"]:
            session["design_assistant"]["dataset"] = "None"
        if key is not None:
            session["design_assistant"]["zero_shot_learner"][key] = value

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)

"""
{
    "design_assistant_config": {
        "zero-shot":
            "campaign" : {
                "uuid": 123,
                "process_step": 2,
                "type": "concrete",
                "powder_config": [360, 370, ...],
            } 
        },
        "dataset": None
    }
}
"""
