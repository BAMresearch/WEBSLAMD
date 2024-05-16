import json

from flask import Blueprint, render_template, request, make_response, jsonify, session

from slamd.design_assistant.processing.design_assistant_service import DesignAssistantService

design_assistant = Blueprint('design_assistant', __name__,
                             template_folder='../templates',
                             static_folder='../static',
                             static_url_path='static',
                             url_prefix='/design_assistant', )


@design_assistant.route('/', methods=['GET'])
def design_assistant_page():
    form, progress = DesignAssistantService.create_design_assistant_form()
    return render_template('design_assistant.html', form=form, progress=progress)


@design_assistant.route('/task', methods=['POST'])
def handle_task():
    task = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(task, 'task')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template("campaign_material_type.html", form=form, session=session)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/material_type', methods=['POST'])
def handle_material():
    material_type = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(material_type, 'type')
    form, progress = DesignAssistantService.create_design_assistant_form()
    template = DesignAssistantService.get_template_of_selected_task()
    body = {'template': render_template(template, form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/design_targets', methods=['POST'])
def handle_design_targets():
    design_targets = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_targets, 'design_targets')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/campaign_design_targets_values.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/design_targets_values', methods=['POST'])
def handle_design_targets_values():
    design_targets_values = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_targets_values, 'design_targets')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/campaign_select_powders.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/powders', methods=['POST'])
def handle_powders():
    powders = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(powders, 'powders')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/campaign_liquids.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/liquid', methods=['POST'])
def handle_liquids():
    liquid = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(liquid, 'liquids')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/campaign_other.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/other', methods=['POST'])
def handle_other():
    other = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(other, 'other')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/comment.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/comment', methods=['POST'])
def handle_comment():
    comment = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(comment, 'comment')
    form, progress = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('zero_shot_learner/design_knowledge.html', form=form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/generate_design_knowledge', methods=['POST'])
def handle_generating_design_knowledge():
    data = json.loads(request.data)
    design_knowledge = DesignAssistantService.generate_design_knowledge(data['token'])
    body = {'template': design_knowledge}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/generate_formulation', methods=['POST'])
def handle_generating_formulation():
    data = json.loads(request.data)
    formulation = DesignAssistantService.generate_formulation(data['design_knowledge'], data['token'])
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/formulation.html', form=form, formulation=formulation)}
    return make_response((jsonify(body)))


@design_assistant.route('/zero_shot/save_formulation', methods=['POST'])
def handle_saving_formulation():
    data = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(data['design_knowledge'], 'design_knowledge')
    DesignAssistantService.update_design_assistant_session(data['formulation'], 'formulation')
    form, _ = DesignAssistantService.create_design_assistant_form()
    body = {'template': render_template('/zero_shot_learner/formulation.html', form=form)}
    return make_response((jsonify(body)))


@design_assistant.route('/new_project/<material_type>', methods=['POST'])
def handle_saving_material(material_type):
    data = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(data, material_type)
    form, progress = DesignAssistantService.create_design_assistant_form()
    template = DesignAssistantService.get_template_of_next_new_project_step(progress)
    body = {'template': render_template(template, form=form, progress=progress)}
    return make_response((jsonify(body)))


@design_assistant.route('/session', methods=['DELETE'])
def handle_delete_session():
    DesignAssistantService.delete_design_assistant_session()
    return jsonify({'message': 'Session deleted successfully'})
