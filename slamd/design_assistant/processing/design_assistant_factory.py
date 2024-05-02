from slamd.design_assistant.processing.forms.campaign_form import CampaignForm
from slamd.design_assistant.processing.forms.design_assistant_form import DesignAssistantForm
from slamd.design_assistant.processing.forms.task_form import TaskForm
from slamd.design_assistant.processing.forms.material_type_form import MaterialTypeForm
from slamd.design_assistant.processing.forms.new_project_form import NewProjectForm


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_form(cls):
        form = DesignAssistantForm()
        return form
    
    @classmethod
    def create_material_type_form(cls):
        form = MaterialTypeForm()
        return form

    @classmethod
    def create_design_assistant_task_form(cls):
        form = TaskForm()
        return form
    
    @classmethod
    def create_design_assistant_campaign_form(cls):
        form = CampaignForm()
        return form
    
    @classmethod
    def create_new_project_assistant_form(cls):
        form = NewProjectForm() 
        return form