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
    return render_template('design_assistant.html', form=form, task_form=form.task_form,
                           campaign_form=form.campaign_form, progress=progress)


@design_assistant.route('/task', methods=['POST'])
def handle_task():
    task = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(task, 'task')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_material_type.html', campaign_form=campaign_form, session=session)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/material_type', methods=['POST'])
def handle_material():
    material_type = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(material_type, 'type')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_design_targets.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/design_targets', methods=['POST'])
def handle_design_targets():
    design_targets = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_targets, 'design_targets')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_design_targets_values.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/design_targets_values', methods=['POST'])
def handle_design_targets_values():
    design_targets_values = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_targets_values, 'design_targets')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_select_powders.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/powders', methods=['POST'])
def handle_powders():
    powders = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(powders, 'powders')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_liquids.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/liquid', methods=['POST'])
def handle_liquids():
    liquid = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(liquid, 'liquid')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('campaign_other.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/other', methods=['POST'])
def handle_other():
    other = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(other, 'other')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('comment.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/comment', methods=['POST'])
def handle_comment():
    comment = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(comment, 'comment')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('design_knowledge.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/generate_design_knowledge', methods=['POST'])
def handle_generating_design_knowledge():
    data = json.loads(request.data)
    design_knowledge = DesignAssistantService.generate_design_knowledge(data['token'])
    body = {'template': design_knowledge}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/design_knowledge', methods=['POST'])
def handle_design_knowledge():
    design_knowledge = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_knowledge, 'design_knowledge')
    body = {'template': render_template('prompt.html')}
    return make_response(jsonify(body), 200)


@design_assistant.route('/zero_shot/generate_formulation', methods=['POST'])
def handle_generating_formulation():
    data = json.loads(request.data)
    formulation = DesignAssistantService.generate_formulation(data['design_knowledge'], data['token']) 
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('formulation.html', campaign_form=campaign_form, formulation=formulation)}
    return make_response((jsonify(body)))


@design_assistant.route('zero_shot/save_formulation', methods=['POST'])
def handle_saving_formulation():
    data = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(data['design_knowledge'], 'design_knowledge')
    DesignAssistantService.update_design_assistant_session(data['formulation'], 'formulation')
    campaign_form = DesignAssistantService.create_design_assistant_campaign_form()
    body = {'template': render_template('formulation.html', campaign_form=campaign_form)}
    return make_response((jsonify(body))) 


@design_assistant.route('/session', methods=['DELETE'])
def handle_delete_session():
    DesignAssistantService.delete_design_assistant_session()
    return jsonify({'message': 'Session deleted successfully'})
