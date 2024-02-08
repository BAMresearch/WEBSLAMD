from flask import Blueprint, render_template, request
import json

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
    form = DesignAssistantService.create_design_assistant_task_form()
    # form = DesignAssistantServiceForm()
    return render_template("design_assistant.html", form=form)


@design_assistant.route("/", methods=["POST"])
def select_design_assistant_task():
    # data = json.loads(request)
    form = DesignAssistantService.create_design_assistant_task_form()
    print(request)
    return render_template("design_assistant.html", form=form)
