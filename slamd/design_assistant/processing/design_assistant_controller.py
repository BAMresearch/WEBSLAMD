from flask import Blueprint, render_template

from slamd.design_assistant.processing.forms.design_assistant_service_form import (
    DesignAssistantServiceForm,
)
from slamd.design_assistant.processing.design_assistant_service import (
    DesignAssistantService,
)

design_assistant = Blueprint(
    "design_assistant",
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="static",
    url_prefix="/design_assistant",
)


@design_assistant.route("/", methods=["GET"])
def design_assistant_page():
    form = DesignAssistantService.create_design_assistant_service_form()
    # form = DesignAssistantServiceForm()
    return render_template("design_assistant.html", form=form)
