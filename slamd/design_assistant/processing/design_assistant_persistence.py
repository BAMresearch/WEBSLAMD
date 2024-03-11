from flask import session

from slamd.common.error_handling import ValueNotSupportedException
from slamd.common.slamd_utils import not_numeric, not_empty


class DesignAssistantPersistence:

    @classmethod
    def init_session(cls):
        session['design_assistant'] = {}

    @classmethod
    def update_session(cls, value, key):
        if key == 'task':
            if value not in ['zero_shot_learner', 'data_creation']:
                raise ValueNotSupportedException('Provided task is not supported.')
            cls._update_session_for_task_key(value)

        if key == 'import_selection':
            # TODO: Story for Session Import
            cls._update_session_for_import_selection_key()

        if key == 'type':
            if value not in ['Concrete', 'Binder']:
                raise ValueNotSupportedException('Provided type is not supported.')
            cls._update_session_for_material_type_key(value)

        if key == 'design_targets':
            target_values = value.values()
            if len(target_values) > 2:
                raise ValueNotSupportedException('Only up to two target values are supported.')
            for item in target_values:
                if not_empty(item) and not_numeric(item):
                    raise ValueNotSupportedException('Only numerical values ar allowed.')
            cls._update_session_for_design_targets_key(value)

        if key == 'powders':
            if not cls._valid_powder_selection(value):
                raise ValueNotSupportedException('Powder selection is not valid.')
            cls._update_session_for_powders_key(value)

        if key == 'liquid':
            cls._update_session_for_liquid_key(value)

        if key == 'other':
            cls._update_session_for_other_key(value)

        if key == 'comment':
            cls._update_session_for_comment_key(value)

    @classmethod
    def _valid_powder_selection(cls, value):
        blend = value['blend_powders']
        selected_powders = value['selected_powders']
        if all(x in ['opc', 'geopolymer', 'ggbfs', 'fly_ash'] for x in selected_powders):
            if len(selected_powders) == 1 and blend == 'no' or len(selected_powders) == 2 and blend in ['yes', 'no']:
                return True
        return False


    @classmethod
    def _update_session_for_task_key(cls, value):
        if value == 'zero_shot_learner':
            session['design_assistant']['zero_shot_learner'] = {}

    @classmethod
    def _update_session_for_import_selection_key(cls):
        session['design_assistant']['dataset'] = 'None'

    @classmethod
    def _update_session_for_design_targets_key(cls, value):
        if isinstance(value, dict):
            design_targets = []
            for k, v in value.items():
                design_targets.append({k: v})
            session['design_assistant']['zero_shot_learner']['design_targets'] = design_targets
        if isinstance(value, list):
            session['design_assistant']['zero_shot_learner']['design_targets'] = value

    @classmethod
    def _update_session_for_material_type_key(cls, value):
        session['design_assistant']['zero_shot_learner']['type'] = value

    @classmethod
    def _update_session_for_powders_key(cls, value_object):
        selected_powders = value_object['selected_powders']
        blend_powders = value_object['blend_powders']
        session['design_assistant']['zero_shot_learner']['powders'] = {'selected': selected_powders,'blend': blend_powders}

    @classmethod
    def _update_session_for_liquid_key(cls, value):
        session['design_assistant']['zero_shot_learner']['liquid'] = value

    @classmethod
    def _update_session_for_other_key(cls, value):
        session['design_assistant']['zero_shot_learner']['other'] = value

    @classmethod
    def _update_session_for_comment_key(cls, value):
        session['design_assistant']['zero_shot_learner']['comment'] = value

    @classmethod
    def get_session_for_property(cls, key):
        return session.get(key)

    @classmethod
    def delete_session_key(cls, key):
        if key in session.keys():
            session.pop(key)