from flask import Blueprint, render_template, request, make_response, jsonify
import json

from slamd.design_assistant.processing.design_assistant_service import (
    DesignAssistantService,
)
from flask import session

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
    return render_template("design_assistant.html", form=form)


@design_assistant.route("/task", methods=["POST"])
def handle_task():
    selection = json.loads(request.data)
    ## handle this selection for when implementing data creation in digital lab
    form = DesignAssistantService.create_design_assistant_import_form()
    body = {"template": render_template("import.html", form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route("/import", methods=["POST"])
def handle_import():
    


@design_assistant.route("/material", methods=["POST"])
def handle_material():
    pass


@design_assistant.route("/target_values", methods=["POST"])
def handle_target_values():
    pass


@design_assistant.route("/powders", methods=["POST"])
def handle_powders():
    pass


@design_assistant.route("/liquids", methods=["POST"])
def handle_liquids():
    pass
