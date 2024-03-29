from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_factory import DesignAssistantFactory
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.llm_service import LLMService


class DesignAssistantService:

    @classmethod
    def create_design_assistant_form(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        progress = cls._extract_progress(design_assistant_session)
        form = DesignAssistantFactory.create_design_assistant_form()
        if not design_assistant_session:
            cls.init_design_assistant_session()
            form.import_form = None
            form.campaign_form = None
        if design_assistant_session:
            if 'zero_shot_learner' in list(design_assistant_session.keys()):
                cls._populate_task_form_with_session_value(form, 'zero_shot_learner')
            if 'zero_shot_learner' in list(design_assistant_session.keys()):
                cls._populate_campaign_form_with_session_value(form, design_assistant_session)
            else:
                form.campaign_form = None
        return form, progress

    @classmethod
    def _extract_progress(cls, design_assistant_session):
        if design_assistant_session:
            if design_assistant_session.get('zero_shot_learner', None):
                return DesignAssistantPersistence.get_progress('zero_shot_learner')
            elif design_assistant_session.get('data_creation', None):
                return DesignAssistantPersistence.get_progress('data_creation')
            return 0
        return 0

    @classmethod
    def _populate_task_form_with_session_value(cls, form, session_value):
        form.task_form.task_field.data = session_value

    @classmethod
    def _populate_campaign_form_with_session_value(cls, form, design_assistant_session):
        for key, value in design_assistant_session['zero_shot_learner'].items():
            if key == 'type':
                cls._populate_material_type_field_with_session_value(form, value)
            if key == 'design_targets':
                cls._populate_design_targets_field_with_session_value(form, value)
            if key == 'powders':
                cls._populate_powders_field_with_session_value(form, value)
            if key == 'liquid':
                cls._populate_liquids_field_with_session_value(form, value)
            if key == 'other':
                cls._populate_other_field_with_session_value(form, value)
            if key == 'comment':
                cls._populate_comment_field_with_session_value(form, value)
            if key == 'design_knowledge':
                cls._populate_design_knowledge_field_with_session_value(form, value)

    @classmethod
    def _populate_design_targets_field_with_session_value(cls, form, value):
        for design_target in value:
            form.campaign_form.design_targets.append_entry(design_target)

    @classmethod
    def _populate_material_type_field_with_session_value(cls, form, session_value):
        form.campaign_form.material_type_field.data = session_value

    @classmethod
    def _populate_powders_field_with_session_value(cls, form, value):
        for (powder_session_key, powder_session_value) in value.items():
            if powder_session_key == 'selected':
                form.campaign_form.select_powders_field.data = powder_session_value
            if powder_session_key == 'blend':
                form.campaign_form.blend_powders_field.data = powder_session_value

    @classmethod
    def _populate_liquids_field_with_session_value(cls, form, value):
        if value in ['pure_water', 'activator_liquid']:
            form.campaign_form.liquids_field.data = value
        else:
            form.campaign_form.additional_liquid.data = value

    @classmethod
    def _populate_other_field_with_session_value(cls, form, value):
        if value in ['scm', 'super_plasticizer']:
            form.campaign_form.other_field.data = value
        else:
            form.campaign_form.additional_other.data = value

    @classmethod
    def _populate_comment_field_with_session_value(cls, form, value):
        form.campaign_form.comment_field.data = value

    @classmethod
    def _populate_design_knowledge_field_with_session_value(cls, form, value):
        form.campaign_form.design_knowledge_field.data = value

    @classmethod
    def create_design_assistant_campaign_form(cls):
        form, _ = cls.create_design_assistant_form()
        return form.campaign_form

    @classmethod
    def init_design_assistant_session(cls):
        DesignAssistantPersistence.init_session()

    @classmethod
    def update_design_assistant_session(cls, value, key=None):
        if key == 'task':
            if value not in ['zero_shot_learner', 'data_creation']:
                raise ValueNotSupportedException('Provided task is not supported.')
            DesignAssistantPersistence.update_session_for_task_key(value)

        if key == 'type':
            if value not in ['Concrete', 'Binder']:
                raise ValueNotSupportedException('Provided type is not supported.')
            DesignAssistantPersistence.update_session_for_material_type_key(value)

        if key == 'design_targets':
            if not cls._valid_targets_selection(value):
                raise ValueNotSupportedException('Invalid target selection.')
            DesignAssistantPersistence.update_session_for_design_targets_key(value)

        if key == 'powders':
            if not cls._valid_powder_selection(value):
                raise ValueNotSupportedException('Powder selection is not valid.')
            DesignAssistantPersistence.update_session_for_powders_key(value)

        if key == 'liquid':
            # TODO: implement AI-based check that input string is sensible
            # For now: Naive Check for the inputs length
            if value not in ['pure_water', 'activator_liquid'] and len(value) > 20:
                raise ValueNotSupportedException('Liquid selection is not valid. If a custom name '
                                                 'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_liquid_key(value)

        if key == 'other':
            # TODO: implement AI-based check that input string is sensible
            # For now: Naive Check for the inputs length
            if value not in ['scm', 'super_plasticizer'] and len(value) > 20:
                raise ValueNotSupportedException('Other selection is not valid. If a custom name '
                                                 'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_other_key(value)

        if key == 'comment':
            # TODO: implement AI-based check that input string is sensible
            DesignAssistantPersistence.update_session_for_comment_key(value)

        if key == 'design_knowledge':
            DesignAssistantPersistence.update_session_for_design_knowledge_key(value)

    @classmethod
    def _valid_powder_selection(cls, value):
        blend = value['blend_powders']
        selected_powders = value['selected_powders']
        if all(x in ['opc', 'geopolymer', 'ggbfs', 'fly_ash'] for x in selected_powders):
            if len(selected_powders) == 1 and blend == 'no' or len(selected_powders) == 2 and blend in ['yes', 'no']:
                return True
        return False

    @classmethod
    def _valid_targets_selection(cls, value):
        if len(value) > 2:
            return False
        for item in value:
            design_target_value_field = item.get('design_target_value_field', None)
            design_target_optimization_field = item.get('design_target_optimization_field', None)
            if design_target_value_field and len(design_target_value_field) > 20:
                return False
            if design_target_optimization_field and design_target_optimization_field not in ['maximized',
                                                                                             'minimized',
                                                                                             'No optimization']:
                return False
        return True

    @classmethod
    def delete_design_assistant_session(cls):
        DesignAssistantPersistence.delete_session_key('design_assistant')

    @classmethod
    def instantiate_da_session_on_upload(cls, session_data):
        DesignAssistantPersistence.delete_session_key('design_assistant')
        DesignAssistantPersistence.init_session()
        if 'zero_shot_learner' in list(session_data.keys()) and 'data_creation' in list(session_data.keys()):
            raise SlamdUnprocessableEntityException(message='Only one campaign, either zero shot or data creation can '
                                                            'be supported simultaneously.')
        if 'zero_shot_learner' in list(session_data.keys()):
            DesignAssistantPersistence.save(session_data, 'zero_shot_learner')
        else:
            pass

    @classmethod
    def generate_design_knowledge(cls, token):
        design_knowledge = LLMService.generate_design_knowledge(token)
        return design_knowledge
