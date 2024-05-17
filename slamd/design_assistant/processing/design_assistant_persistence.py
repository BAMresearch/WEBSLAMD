from flask import session

ZERO_SHOT_STEPS = 10
DATA_CREATION_STEPS = 17


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session['design_assistant'] = {}

    @classmethod
    def update_session_for_task_key(cls, value):
        session['design_assistant'][value] = {}
        session['design_assistant'][value]["progress"] = 1

    @classmethod
    def update_session_for_design_targets_key(cls, value):
        session['design_assistant']['zero_shot_learner']['design_targets'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_material_type_key(cls, value):
        design_assistant_session = session['design_assistant']
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            session['design_assistant']['zero_shot_learner']['type'] = value
        if 'data_creation' in list(design_assistant_session.keys()):
            session['design_assistant']['data_creation']['type'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_powders_key(cls, value_object):
        selected_powders = value_object['selected_powders']
        blend_powders = value_object['blend_powders']
        session['design_assistant']['zero_shot_learner']['powders'] = {'selected': selected_powders,
                                                                       'blend': blend_powders}
        cls.update_progress()

    @classmethod
    def update_session_for_liquids_key(cls, value):
        session['design_assistant']['zero_shot_learner']['liquids'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_other_key(cls, value):
        session['design_assistant']['zero_shot_learner']['other'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_comment_key(cls, value):
        session['design_assistant']['zero_shot_learner']['comment'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_design_knowledge_key(cls, value):
        session['design_assistant']['zero_shot_learner']['design_knowledge'] = value
        cls.update_progress()

    @classmethod
    def update_session_for_formulation_key(cls, value):
        session['design_assistant']['zero_shot_learner']['formulation'] = value
        cls.update_progress()
    
    @classmethod
    def update_session_for_materials_key(cls, materials):
        session['design_assistant']['data_creation']['materials'] = materials
        cls.update_progress()

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)
    
    @classmethod
    def get_data_creation_session(cls):
        return session['design_assistant']['data_creation']

    @classmethod
    def delete_session_key(cls, key):
        if key in session.keys():
            session.pop(key)

    @classmethod
    def save(cls, session_data, task):
        session['design_assistant'][task] = session_data[task]
        material_type = session_data[task].get('type', None)
        if material_type:
            session['design_assistant']['type'] = session_data[task]['type']

    @classmethod
    def get_progress(cls, task):
        progress = session['design_assistant'][task].get("progress", None)
        if progress:
            return session['design_assistant'][task]["progress"]
        return 0

    @classmethod
    def update_progress(cls):
        design_assistant_session = session["design_assistant"]
        if 'data_creation' in list(design_assistant_session.keys()):
            current_progress = session['design_assistant']['data_creation']["progress"]
            task = 'data_creation'
            if current_progress < DATA_CREATION_STEPS:
                session['design_assistant'][task]["progress"] += 1
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            current_progress = session['design_assistant']['zero_shot_learner']["progress"]
            task = 'zero_shot_learner'
            if current_progress < ZERO_SHOT_STEPS:
                session['design_assistant'][task]["progress"] += 1

    @classmethod
    def get_free_llm_calls_count(cls):
        return session.get('count_llm_calls', 0)

    @classmethod
    def update_remaining_free_llm_calls(cls):
        session['count_llm_calls'] = session.get('count_llm_calls', 0) + 1
