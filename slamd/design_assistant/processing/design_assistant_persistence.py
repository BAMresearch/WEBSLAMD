from flask import session


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session["design_assistant"] = {}

    @classmethod
    def update_session(cls, value, key=None):
        if value in ["zero_shot_learner"]:
            session["design_assistant"]["zero_shot_learner"] = {}
        if value in ["no_import"]:
            session["design_assistant"]["dataset"] = "None"
        else:
            session["design_assistant"]["zero_shot_learner"][key] = value


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
