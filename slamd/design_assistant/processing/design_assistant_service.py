from slamd.design_assistant.processing.design_assistant_factory import DesignAssistantFactory
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence


class DesignAssistantService:

    @classmethod
    def create_design_assistant_form(cls):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        form = DesignAssistantFactory.create_design_assistant_form()
        if not design_assistant_session:
            cls.init_design_assistant_session()
            form.import_form = None
            form.campaign_form = None
        if design_assistant_session:
            if 'zero_shot_learner' in list(design_assistant_session.keys()):
                cls.populate_task_form_with_session_value(form, 'zero_shot_learner')
            if 'dataset' in list(design_assistant_session.keys()):
                cls.populate_import_selection_form_with_session_value(form, design_assistant_session)
            if 'zero_shot_learner' in list(design_assistant_session.keys()):
                cls.populate_campaign_form_with_session_value(form, design_assistant_session)
            else:
                form.campaign_form = None
        return form

    @classmethod
    def populate_task_form_with_session_value(cls, form, session_value):
        form.task_form.task_field.data = session_value

    @classmethod
    def populate_import_selection_form_with_session_value(cls, form, design_assistant_session):
        form.import_form.import_selection_field.data = design_assistant_session['dataset']

    @classmethod
    def populate_campaign_form_with_session_value(cls, form, design_assistant_session):
        for key, value in design_assistant_session[
            'zero_shot_learner'
        ].items():
            if key == 'type':
                cls.populate_material_type_field_with_session_value(form, value)
            if key == 'design_targets':
                cls.populate_design_targets_field_with_session_value(form, value)
            if key == 'powders':
                cls.populate_powders_field_with_session_value(form, value)
            if key == 'liquid':
                cls.populate_liquids_field_with_session_value(form, value)
            if key == 'other':
                cls.populate_other_field_with_session_value(form, value)
            if key == 'comment':
                cls.populate_comment_field_with_session_value(form, value)

    @classmethod
    def create_design_assistant_task_form(cls):
        form = DesignAssistantFactory.create_design_assistant_task_form()
        return form

    @classmethod
    def create_design_assistant_import_selection_form(cls):
        form = DesignAssistantFactory.create_design_assistant_import_selection_form()
        return form
    
    @classmethod
    def populate_design_targets_field_with_session_value(cls, form, value):
        design_target_options = []
        for design_target in value:
            design_target_option = list(design_target.keys())[0]
            design_target_options.append(design_target_option)
            design_target_value = list(design_target.values())[0]
            if design_target_option in ['strength','workability','reactivity','sustainability','cost']:
                if design_target_option == 'strength':
                    form.campaign_form.target_strength_field.data = design_target_value
                if design_target_option == 'workability':
                    form.campaign_form.target_workability_field.data = design_target_value
                if design_target_option == 'reactivity':
                    form.campaign_form.target_reactivity_field.data = design_target_value
                if design_target_option == 'sustainability':
                    form.campaign_form.target_sustainability_field.data = design_target_value
                if design_target_option == 'cost':
                    form.campaign_form.target_cost_field.data = design_target_value
            else:
                if form.campaign_form.additional_design_targets:
                    form.campaign_form.additional_design_targets.append({'name': design_target_option, 'target_value': design_target_value})
                else:
                    form.campaign_form.additional_design_targets = [{'name': design_target_option, 'target_value': design_target_value}]
        form.campaign_form.design_targets_field.data = design_target_options

    @classmethod
    def populate_material_type_field_with_session_value(cls, form, session_value):
        form.campaign_form.material_type_field.data = session_value

    @classmethod
    def populate_powders_field_with_session_value(cls, form, value):
        for ( powder_session_key, powder_session_value) in value.items():
            if powder_session_key == 'selected':
                form.campaign_form.select_powders_field.data = powder_session_value
            if powder_session_key == 'blend':
                form.campaign_form.blend_powders_field.data = powder_session_value

    @classmethod
    def populate_liquids_field_with_session_value(cls, form, value):
        if value in ['pure_water', 'activator_liquid']:
            form.campaign_form.liquids_field.data = value
        else:
            form.campaign_form.additional_liquid.data = value

    @classmethod
    def populate_other_field_with_session_value(cls, form, value):
        if value in ['scm', 'super_plasticizer']:
            form.campaign_form.other_field.data = value
        else:
            form.campaign_form.additional_other.data = value

    @classmethod
    def populate_comment_field_with_session_value(cls, form, value):
        form.campaign_form.comment_field.data = value

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
    def delete_design_assistant_session(cls):
        DesignAssistantPersistence.delete_session_key('design_assistant')