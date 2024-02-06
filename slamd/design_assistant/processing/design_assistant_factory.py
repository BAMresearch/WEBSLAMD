from slamd.design_assistant.processing.forms.design_assistant_service_form import (
    DesignAssistantServiceForm,
)


class DesignAssistantFactory:

    @classmethod
    def create_design_assistant_service_form(cls):
        form = DesignAssistantServiceForm()
        return form
