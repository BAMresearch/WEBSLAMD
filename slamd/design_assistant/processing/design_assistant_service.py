from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.common.error_handling import ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_factory import DesignAssistantFactory
from slamd.design_assistant.processing.design_assistant_persistence import DesignAssistantPersistence
from slamd.design_assistant.processing.llm_service import LLMService
from slamd.materials.processing.materials_facade import MaterialsFacade


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
                cls._populate_create_project_form_with_session_value(form)
                form.campaign_form = None
        else:
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
    def _populate_create_project_form_with_session_value(cls, form):
        dc_session = DesignAssistantPersistence.get_data_creation_session()
        for key in list(dc_session.keys()):
            if key == 'materials':
                for material, material_id in dc_session['materials'].items():
                    if material == 'powder':
                        cls._populate_create_powder_form_with_session_value(dc_session, form)
                    if material == 'liquid':
                        cls._populate_create_liquid_form_with_session_value(dc_session, form)
                    if material == 'aggregate':
                        cls._populate_create_aggregate_form_with_session_value(dc_session, form)
                    if material == 'admixture':
                        cls._populate_create_admixture_form_with_session_value(dc_session, form)
                    if material == 'process':
                        cls._populate_create_process_form_with_session_value(dc_session, form)

    @classmethod
    def _populate_create_powder_form_with_session_value(cls, dc_session, form):
        powder_uuid = dc_session['materials']['powder']
        powder = MaterialsFacade.get_material_from_session('Powder', powder_uuid)
        if powder.name:
            cls._populate_create_powder_name_field_with_session_value(form, powder.name)
        if powder.costs:
            cls._populate_create_powder_cost_fields_with_session_value(form, powder.costs)
        if powder.composition:
            cls._populate_create_powder_composition_fields_with_session_value(form, powder.composition)
        if powder.structure:
            cls._populate_create_powder_structure_fields_with_session_value(form, powder.structure)

    @classmethod
    def _populate_create_liquid_form_with_session_value(cls, dc_session, form):
        liquid_uuid = dc_session['materials']['liquid']
        liquid = MaterialsFacade.get_material_from_session('Liquid', liquid_uuid)
        if liquid.name:
            cls._populate_create_liquid_name_field_with_session_value(form, liquid.name)
        if liquid.costs:
            cls._populate_create_liquid_cost_fields_with_session_value(form, liquid.costs)
        if liquid.composition:
            cls._populate_create_liquid_composition_fields_with_session_value(form, liquid.composition)
    
    @classmethod
    def _populate_create_aggregate_form_with_session_value(cls, dc_session, form):
        aggregate_uuid = dc_session['materials']['aggregate']
        aggregate = MaterialsFacade.get_material_from_session('Aggregates', aggregate_uuid)
        if aggregate.name:
            cls._populate_create_aggregate_name_field_with_session_value(form, aggregate.name)
        if aggregate.costs:
            cls._populate_create_aggregate_costs_field_with_session_value(form, aggregate.costs)
    
    @classmethod
    def _populate_create_admixture_form_with_session_value(cls, dc_session, form):
        admixture_uuid = dc_session['materials']['admixture']
        admixture = MaterialsFacade.get_material_from_session('Admixture', admixture_uuid)
        if admixture.name:
            cls._populate_create_admixture_name_field_with_session_value(form, admixture.name)
        if admixture.costs:
            cls._populate_create_admixture_costs_field_with_session_value(form, admixture.costs)

    @classmethod
    def _populate_create_process_form_with_session_value(cls, dc_session, form):
        process_uuid = dc_session['materials']['process']
        process = MaterialsFacade.get_material_from_session('Process', process_uuid)
        if process.name:
            cls._populate_create_process_name_field_with_session_value(form, process.name)
        if process.costs:
            cls._populate_create_process_cost_field_with_session_value(form, process.costs)
        if process.duration:
            cls._populate_create_process_duration_field_with_session_value(form, process.duration)
        if process.temperature:
            cls._populate_create_process_temperature_field_with_session_value(form, process.temperature)
        if process.relative_humidity:
            cls._populate_create_process_relative_humidity_field_with_session_value(form, process.relative_humidity)

    @classmethod
    def _populate_create_powder_name_field_with_session_value(cls, form, powder_name):
        form.new_project_form.create_powder_form.name_field.data = powder_name

    @classmethod
    def _populate_create_powder_cost_fields_with_session_value(cls, form, powder_costs):
        form.new_project_form.create_powder_form.cost_CO_2.data = powder_costs.co2_footprint
        form.new_project_form.create_powder_form.cost_EUR.data = powder_costs.costs
        form.new_project_form.create_powder_form.cost_delivery_time.data = powder_costs.delivery_time
        form.new_project_form.create_powder_form.cost_recyclingrate.data = powder_costs.recyclingrate

    @classmethod
    def _populate_create_powder_composition_fields_with_session_value(cls, form, powder_composition):
        form.new_project_form.create_powder_form.Fe_2O_3.data = powder_composition.fe3_o2
        form.new_project_form.create_powder_form.si_o2.data = powder_composition.si_o2
        form.new_project_form.create_powder_form.al2_o3.data = powder_composition.al2_o3
        form.new_project_form.create_powder_form.ca_o.data = powder_composition.ca_o

    @classmethod
    def _populate_create_powder_structure_fields_with_session_value(cls, form, powder_structure):
        form.new_project_form.create_powder_form.fines_modulus.data = powder_structure.fine

    @classmethod
    def _populate_create_liquid_name_field_with_session_value(cls, form, liquid_name):
        form.new_project_form.create_liquid_form.name_field.data = liquid_name

    @classmethod
    def _populate_create_liquid_cost_fields_with_session_value(cls, form, liquid_costs):
        form.new_project_form.create_liquid_form.cost_CO_2.data = liquid_costs.co2_footprint
        form.new_project_form.create_liquid_form.cost_EUR.data = liquid_costs.costs
        form.new_project_form.create_liquid_form.cost_delivery_time.data = liquid_costs.delivery_time
        form.new_project_form.create_liquid_form.cost_recyclingrate.data = liquid_costs.recyclingrate

    @classmethod
    def _populate_create_liquid_composition_fields_with_session_value(cls, form, liquid_composition):
        form.new_project_form.create_liquid_form.h2_O.data = liquid_composition.h2_o
        form.new_project_form.create_liquid_form.h2_O_mol.data = liquid_composition.h2_o_mol
        form.new_project_form.create_liquid_form.na2_si_o3.data = liquid_composition.na2_si_o3
        form.new_project_form.create_liquid_form.na2_si_o3_mol.data = liquid_composition.na2_si_o3_mol
        form.new_project_form.create_liquid_form.na_o_h.data = liquid_composition.na_o_h
        form.new_project_form.create_liquid_form.na_o_h_mol.data = liquid_composition.na_o_h_mol

    @classmethod
    def _populate_create_aggregate_name_field_with_session_value(cls, form, aggregate_name):
        form.new_project_form.create_aggregate_form.name_field.data = aggregate_name

    @classmethod
    def _populate_create_aggregate_costs_field_with_session_value(cls, form, aggregate_costs):
        form.new_project_form.create_aggregate_form.cost_CO_2.data = aggregate_costs.co2_footprint
        form.new_project_form.create_aggregate_form.cost_EUR.data = aggregate_costs.costs
        form.new_project_form.create_aggregate_form.cost_delivery_time.data = aggregate_costs.delivery_time
        form.new_project_form.create_aggregate_form.cost_recyclingrate.data = aggregate_costs.recyclingrate

    @classmethod
    def _populate_create_admixture_name_field_with_session_value(cls, form, admixture_name):
        form.new_project_form.create_admixture_form.name_field.data = admixture_name

    @classmethod
    def _populate_create_admixture_costs_field_with_session_value(cls, form, admixture_costs):
        form.new_project_form.create_admixture_form.cost_CO_2.data = admixture_costs.co2_footprint
        form.new_project_form.create_admixture_form.cost_EUR.data = admixture_costs.costs
        form.new_project_form.create_admixture_form.cost_delivery_time.data = admixture_costs.delivery_time
        form.new_project_form.create_admixture_form.cost_recyclingrate.data = admixture_costs.recyclingrate

    @classmethod
    def _populate_create_process_name_field_with_session_value(cls, form, process_name):
        form.new_project_form.create_process_form.name_field.data = process_name

    @classmethod
    def _populate_create_process_cost_field_with_session_value(cls, form, process_costs):
        form.new_project_form.create_process_form.cost_CO_2.data = process_costs.co2_footprint
        form.new_project_form.create_process_form.cost_EUR.data = process_costs.costs
        form.new_project_form.create_process_form.cost_delivery_time.data = process_costs.delivery_time
    
    @classmethod
    def _populate_create_process_duration_field_with_session_value(cls, form, process_duration):
        form.new_project_form.create_process_form.duration.data = process_duration

    @classmethod
    def _populate_create_process_temperature_field_with_session_value(cls, form, process_temperature):
        form.new_project_form.create_process_form.temperature.data = process_temperature

    @classmethod
    def _populate_create_process_relative_humidity_field_with_session_value(cls, form, process_relative_humidity):
        form.new_project_form.create_process_form.relative_humidity.data = process_relative_humidity

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
            if liquid in ['Water', 'Activator Liquid', 'Activator Solution']:
                liquids.append(liquid)
            else:
                form.campaign_form.additional_liquid.data = liquid
        if liquids:
            form.campaign_form.liquids_field.data = value

    @classmethod
    def _populate_other_field_with_session_value(cls, form, value):
        others = []
        for other in value:
            if other in ["Biochar", "Rice Husk Ash", "Recycled Aggregates", "Limestone Powder", "Recycled Glass Fines",
                         "Super Plasticizer"]:
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
            # For now: Naive Check for the inputs length
            for liquid in value:
                if liquid not in ['Water', 'Activator Liquid', 'Activator Solution'] and len(value) > 30:
                    raise ValueNotSupportedException('Liquid selection is not valid. If a custom name '
                                                     'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_liquids_key(value)

        if key == 'other':
            # For now: Naive Check for the inputs length
            for other in value:
                if other not in ['Biochar', 'Recycled Aggregates', 'Limestone', 'Recycled Glass Fines',
                                 'Super Plasticizer'] and len(value) > 30:
                    raise ValueNotSupportedException('Other selection is not valid. If a custom name '
                                                     'shall be given, it cannot be longer than 20 characters.')
            DesignAssistantPersistence.update_session_for_other_key(value)

        if key == 'comment':
            DesignAssistantPersistence.update_session_for_comment_key(value)

        if key == 'design_knowledge':
            DesignAssistantPersistence.update_session_for_design_knowledge_key(value)

        if key == "formulation":
            DesignAssistantPersistence.update_session_for_formulation_key(value)

        if key == 'powder':
            design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
            materials = design_assistant_session['data_creation'].get('materials', None)
            if materials:
                uuid = design_assistant_session['data_creation']['materials']['powder']
                cls._edit_material(uuid, value)
            else:
                uuid = MaterialsFacade.save_material(value)
                materials = {'powder': str(uuid)}
                DesignAssistantPersistence.update_session_for_materials_key(materials)

        if key == 'liquid':
            design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
            materials = design_assistant_session['data_creation'].get('materials', None)
            uuid = cls._get_uuid_of_material('liquid')
            if uuid:
                cls._edit_material(uuid, value)
            else:
                uuid = MaterialsFacade.save_material(value)
                materials['liquid'] = str(uuid)
                DesignAssistantPersistence.update_session_for_materials_key(materials)
            
        if key == 'aggregate':
            design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
            materials = design_assistant_session['data_creation'].get('materials', None)
            uuid = cls._get_uuid_of_material('aggregate')
            if uuid:
                cls._edit_material(uuid, value)
            else:
                uuid = MaterialsFacade.save_material(value)
                materials['aggregate'] = str(uuid)
                DesignAssistantPersistence.update_session_for_materials_key(materials)
        
        if key == 'admixture':
            design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
            materials = design_assistant_session['data_creation'].get('materials', None)
            uuid = cls._get_uuid_of_material('admixture')
            if uuid:
                cls._edit_material(uuid, value)
            else:
                uuid = MaterialsFacade.save_material(value)
                materials['admixture'] = str(uuid)
                DesignAssistantPersistence.update_session_for_materials_key(materials)
        
        if key == 'process':
            design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
            materials = design_assistant_session['data_creation'].get('materials', None)
            uuid = cls._get_uuid_of_material('process')
            if uuid:
                cls._edit_material(uuid, value)
            else:
                uuid = MaterialsFacade.save_material(value)
                materials['process'] = str(uuid)
                DesignAssistantPersistence.update_session_for_materials_key(materials)

    
    @classmethod
    def _get_uuid_of_material(cls, material):
        design_assistant_session = DesignAssistantPersistence.get_session_for_property("design_assistant")
        uuid = design_assistant_session['data_creation']['materials'].get(material, None)
        return uuid
        
    @classmethod
    def _edit_material(cls, uuid, value):
        MaterialsFacade.edit_material(uuid, value)
        DesignAssistantPersistence.update_progress()
    
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
        elif 'data_creation' in list(session_data.keys()):
            DesignAssistantPersistence.save(session_data, 'data_creation')
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
        design_assistant_session = DesignAssistantPersistence.get_session_for_property('design_assistant')
        if 'data_creation' in list(design_assistant_session.keys()):
            template = '/data_creation/powder_name.html'
        if 'zero_shot_learner' in list(design_assistant_session.keys()):
            template = '/zero_shot_learner/campaign_design_targets.html'
        return template

    @classmethod
    def get_template_of_next_new_project_step(cls, progress):
        template = ''
        if progress == 3:
            template = 'data_creation/powder_costs.html'
        if progress == 4:
            template = 'data_creation/powder_oxide_composition.html'
        if progress == 5:
            template = 'data_creation/powder_structural_composition.html'
        if progress == 6:
            template = 'data_creation/liquid_name.html'
        if progress == 7:
            template = 'data_creation/liquid_costs.html'
        if progress == 8:
            template = 'data_creation/liquid_oxide_composition.html'
        if progress == 9:
            template = 'data_creation/aggregate_name.html'
        if progress == 10:
            template = 'data_creation/aggregate_costs.html'        
        if progress == 11:
            template = 'data_creation/aggregate_composition.html'
        if progress == 12:
            template = 'data_creation/admixture_name.html'
        if progress == 13:
            template = 'data_creation/admixture_costs.html'  
        if progress == 14:
            template = 'data_creation/process_name.html'
        if progress == 15:
            template = 'data_creation/process_costs.html'
        if progress == 16:
            template = 'data_creation/process_information.html'
        if progress == 17:
            template = 'data_creation/formulation.html' 
        return template