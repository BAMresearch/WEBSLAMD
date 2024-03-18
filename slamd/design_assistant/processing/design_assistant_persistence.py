from flask import session


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session['design_assistant'] = {}

    @classmethod
    def update_session_for_task_key(cls, value):
        session['design_assistant'][value] = {}


    @classmethod
    def update_session_for_import_selection_key(cls):
        session['design_assistant']['dataset'] = 'None'

    @classmethod
    def update_session_for_design_targets_key(cls, value):
        if isinstance(value, dict):
            design_targets = []
            for k, v in value.items():
                design_targets.append({k: v})
            session['design_assistant']['zero_shot_learner']['design_targets'] = design_targets
        if isinstance(value, list):
            session['design_assistant']['zero_shot_learner']['design_targets'] = value

    @classmethod
    def update_session_for_material_type_key(cls, value):
        session['design_assistant']['zero_shot_learner']['type'] = value

    @classmethod
    def update_session_for_powders_key(cls, value_object):
        selected_powders = value_object['selected_powders']
        blend_powders = value_object['blend_powders']
        session['design_assistant']['zero_shot_learner']['powders'] = {'selected': selected_powders,
                                                                       'blend': blend_powders}

    @classmethod
    def update_session_for_liquid_key(cls, value):
        session['design_assistant']['zero_shot_learner']['liquid'] = value

    @classmethod
    def update_session_for_other_key(cls, value):
        session['design_assistant']['zero_shot_learner']['other'] = value

    @classmethod
    def update_session_for_comment_key(cls, value):
        session['design_assistant']['zero_shot_learner']['comment'] = value

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)

    @classmethod
    def delete_session_key(cls, key):
        if key in session.keys():
            session.pop(key)

    @classmethod
    def save(cls, session_data, task):
        session['design_assistant'][task] = session_data[task]
        session['design_assistant']['dataset'] = 'None'
        session['design_assistant']['type'] = session_data[task]['type']
