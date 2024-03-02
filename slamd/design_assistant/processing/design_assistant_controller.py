from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    jsonify,
    session,
    redirect,
)
import json

from slamd.design_assistant.processing.design_assistant_service import (
    DesignAssistantService,
)
from slamd.design_assistant.processing.design_assistant_persistence import (
    DesignAssistantPersistence,
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
    print(session)
    return render_template(
        "design_assistant.html",
        form=form,
        task_form=form.task_form,
        import_form=form.import_form,
        campaign_form=form.campaign_form,
    )


@design_assistant.route("/task", methods=["POST"])
def handle_task():
    task = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(task)
    import_form = DesignAssistantService.create_design_assistant_import_selection_form()
    body = {
        "template": render_template("import_selection.html", import_form=import_form)
    }
    print(session)

    return make_response(jsonify(body), 200)


@design_assistant.route("/import_selection", methods=["POST"])
def handle_import():
    import_selection = json.loads(request.data)
    print(import_selection)
    DesignAssistantService.update_design_assistant_session(import_selection)
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {
        "template": render_template(
            "campaign_material_type.html",
            campaign_form=campaign_form,
            session=session,
        )
    }
    print(session)
    return make_response(jsonify(body), 200)


@design_assistant.route("/material_type", methods=["POST"])
def handle_material():
    material_type = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(material_type, "type")
    print(session)
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {
        "template": render_template(
            "campaign_design_targets.html", campaign_form=campaign_form
        )
    }
    return make_response(jsonify(body), 200)


@design_assistant.route("/design_targets", methods=["POST"])
def handle_target_values():
    design_targets = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(
        design_targets, "design_targets"
    )
    print(session)
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {
        "template": render_template(
            "campaign_select_powders.html", campaign_form=campaign_form
        )
    }
    return make_response(jsonify(body), 200)


@design_assistant.route("/powders", methods=["POST"])
def handle_powders():
    powders = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(powders, "powders")
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {
        "template": render_template(
            "campaign_liquids.html", campaign_form=campaign_form
        )
    }
    print(session)
    return make_response(jsonify(body), 200)


@design_assistant.route("/liquid", methods=["POST"])
def handle_liquids():
    liquid = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(liquid, "liquid")
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {
        "template": render_template("campaign_other.html", campaign_form=campaign_form)
    }
    print(session)
    return make_response(jsonify(body), 200)


@design_assistant.route("/delete_session", methods=["POST"])
def handle_delete_session():
    print("redirecting...")
    DesignAssistantService.delete_design_assistant_session()
    return redirect("/")
