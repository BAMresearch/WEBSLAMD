from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_factory import DesignAssistantFactory
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.llm_service import LLMService
from flask import render_template

class DesignAssistantService:

    @classmethod
    def create_design_assistant_form(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        progress = cls._extract_progress(design_assistant_session)
        form = DesignAssistantFactory.create_design_assistant_form()
        if design_assistant_session:
            if 'zero_shot_learner' in list(design_assistant_session.keys()):             
                cls._populate_task_form_with_session_value(form, 'zero_shot_learner')
                cls._populate_material_type_form_with_session_value(form, design_assistant_session, 'zero_shot_learner')
                cls._populate_campaign_form_with_session_value(form, design_assistant_session)
                form.new_project_form = None
            if 'data_creation' in list(design_assistant_session.keys()):
                cls._populate_task_form_with_session_value(form, 'data_creation') 
                cls._populate_material_type_form_with_session_value(form, design_assistant_session, 'data_creation')
                form.campaign_form = None
        if not design_assistant_session:
            cls.init_design_assistant_session()
            form = DesignAssistantFactory.create_design_assistant_form()
            form.material_type_form = None
            form.campaign_form = None
            form.new_project_form = None
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
    def _populate_material_type_form_with_session_value(cls, form, design_assistant_session, task):
        for key, value in design_assistant_session[task].items():
            if key == 'type':
                form.material_type_form.material_type_field.data = value

    @classmethod
    def _populate_campaign_form_with_session_value(cls, form, design_assistant_session):
        for key, value in design_assistant_session['zero_shot_learner'].items():
            if key == 'design_targets':
                cls._populate_design_targets_field_with_session_value(form, value)
            if key == 'powders':
                cls._populate_powders_field_with_session_value(form, value)
            if key == 'liquids':
                cls._populate_liquids_field_with_session_value(form, value)
            if key == 'other':
                cls._populate_other_field_with_session_value(form, value)
            if key == 'comment':
                cls._populate_comment_field_with_session_value(form, value)
            if key == 'design_knowledge':
                cls._populate_design_knowledge_field_with_session_value(form, value)
            if key == 'formulation':
                cls._populate_formulation_field_with_session_value(form, value)

    @classmethod
    def _populate_design_targets_field_with_session_value(cls, form, value):
        for design_target in value:
            form.campaign_form.design_targets.append_entry(design_target)

    @classmethod
    def _populate_powders_field_with_session_value(cls, form, value):
        for (powder_session_key, powder_session_value) in value.items():
            if powder_session_key == 'selected':
                form.campaign_form.select_powders_field.data = powder_session_value
            if powder_session_key == 'blend':
                form.campaign_form.blend_powders_field.data = powder_session_value

    @classmethod
    def _populate_liquids_field_with_session_value(cls, form, value):
        liquids = []
        for liquid in value:
            if liquid in ['Water', 'Activator Liquid','Activator Solution']:
                liquids.append(liquid)
            else:
                form.campaign_form.additional_liquid.data = liquid
        if liquids:
            form.campaign_form.liquids_field.data = value

    @classmethod
    def _populate_other_field_with_session_value(cls, form, value):
        others = []
        for other in value:
            if other in [ "Biochar", "Rice Husk Ash", "Recycled Aggregates" , "Limestone Powder", "Recycled Glass Fines", "Super Plasticizer"]:
                others.append(other)
            else:
                form.campaign_form.additional_other.data = other
        form.campaign_form.other_field.data = others

    @classmethod
    def _populate_comment_field_with_session_value(cls, form, value):
        form.campaign_form.comment_field.data = value

    @classmethod
    def _populate_design_knowledge_field_with_session_value(cls, form, value):
        form.campaign_form.design_knowledge_field.data = value
    
    @classmethod
    def _populate_formulation_field_with_session_value(cls, form, value):
        form.campaign_form.formulation_field.data = value

    @classmethod
    def create_design_assistant_campaign_form(cls):
        form, _ = cls.create_design_assistant_form()
        return form.campaign_form

    @classmethod
    def create_design_assistant_new_project_form(cls):
        pass

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

        if key == 'liquids':
            # TODO: implement AI-based check that input string is sensible
            # For now: Naive Check for the inputs length
            for liquid in value:
                if liquid not in ['Water', 'Activator Liquid', 'Activator Solution'] and len(value) > 30:
                    raise ValueNotSupportedException('Liquid selection is not valid. If a custom name '
                                                    'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_liquids_key(value)

        if key == 'other':
            # TODO: implement AI-based check that input string is sensible
            # For now: Naive Check for the inputs length
            for other in value:
                if other not in ['Biochar', 'Recycled Aggregates', 'Limestone', 'Recycled Glass Fines', 'Super Plasticizer'] and len(value) > 30:
                    raise ValueNotSupportedException('Other selection is not valid. If a custom name '
                                                    'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_other_key(value)

        if key == 'comment':
            # TODO: implement AI-based check that input string is sensible
            DesignAssistantPersistence.update_session_for_comment_key(value)

        if key == 'design_knowledge':
            DesignAssistantPersistence.update_session_for_design_knowledge_key(value)
        
        if key == "formulation":
            DesignAssistantPersistence.update_session_for_formulation_key(value)

    @classmethod
    def _valid_powder_selection(cls, value):
        blend = value['blend_powders']
        selected_powders = value['selected_powders']
        if all(x in ['OPC', 'Geopolymer', 'GGBFS', 'Fly Ash'] for x in selected_powders):
            if len(selected_powders) == 1 and blend == 'No' or len(selected_powders) == 2 and blend in ['Yes', 'No']:
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
            if design_target_optimization_field and design_target_optimization_field not in ['increase',
                                                                                             'decrease',
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

    @classmethod
    def generate_formulation(cls, design_knowledge, token):
        formulations = LLMService.generate_formulation(design_knowledge, token) 
        return formulations
    
    @classmethod
    def get_template_of_selected_task(cls):
        template = ''
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        if 'data_creation' in list(design_assistant_session.keys()): 
            template = 'create_powders.html'
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            template = 'campaign_design_targets.html'
        return template
    
    @classmethod
    def get_form_of_selected_task(cls):
        form = None
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        if 'data_creation' in list(design_assistant_session.keys()): 
            form = cls.create_design_assistant_new_project_form()
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            form = cls.create_design_assistant_campaign_form()    
        return form 
    
    @classmethod
    def return_template_of_selected_task(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        if 'data_creation' in list(design_assistant_session.keys()): 
            template = 'create_powders.html'
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            template = 'campaign_design_targets.html'
        return template 