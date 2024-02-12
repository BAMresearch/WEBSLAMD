from flask import Blueprint, render_template, request, make_response, jsonify
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
    form = DesignAssistantService.create_design_assistant_form()
    # form = DesignAssistantServiceForm()
    return render_template("design_assistant.html", form=form)


# @design_assistant.route("/", methods=["POST"])
# def select_design_assistant_task():
#     design_task_selection = json.loads(request.data)
#     # form = DesignAssistantService.create_design_assistant_task_form()
#     print(json.loads(request.data))
#     return render_template("design_assistant.html", form=form)


@design_assistant.route("/select_task", methods=["POST"])
def select_design_assistant_task():
    design_task_selection = json.loads(request.data)
    print(design_task_selection)
    # DesignAssistantService.update_design_assistant_chat(design_task_selection)
    # form = DesignAssistantService.create_design_assistant_task_form()
    # body = {"template": render_template("design_assistant.html", form=form)}
    # return make_response(jsonify(body), 200)
    # return render_template("design_assistant.html", form=form)
