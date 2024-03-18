import json
from flask import Blueprint, render_template, request, make_response, jsonify, session

from slamd.common.error_handling import SlamdUnprocessableEntityException, ValueNotSupportedException
from slamd.design_assistant.processing.design_assistant_service import DesignAssistantService

design_assistant = Blueprint('design_assistant', __name__,
                             template_folder='../templates',
                             static_folder='../static',
                             static_url_path='static',
                             url_prefix='/design_assistant', )


@design_assistant.route('/', methods=['GET'])
def design_assistant_page():
    form = DesignAssistantService.create_design_assistant_form()
    return render_template('design_assistant.html', form=form, task_form=form.task_form,

                           campaign_form=form.campaign_form )


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
def handle_target_values():
    design_targets = json.loads(request.data)
    DesignAssistantService.update_design_assistant_session(design_targets, 'design_targets')
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
    body = {'template': render_template('knowledge.html', campaign_form=campaign_form)}
    return make_response(jsonify(body), 200)


@design_assistant.route('/session', methods=['DELETE'])
def handle_delete_session():
    DesignAssistantService.delete_design_assistant_session()
    return jsonify({'message': 'Session deleted successfully'})


@design_assistant.route('/save', methods=['GET'])
def save_da_session():
    json_string = DesignAssistantService.convert_da_session_to_json_string()
    response = make_response(json_string.encode())
    filename = DesignAssistantService.create_default_filename()
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.mimetype = 'text/json'
    return response


@design_assistant.route('/upload', methods=['POST'])
def upload_da_session():
    if 'file' not in request.files:
        raise SlamdUnprocessableEntityException(message='Request did not contain a file')

    file_extension = request.files['file'].filename.lower().split('.')[-1]
    if file_extension != 'json':
        raise ValueNotSupportedException(message=f'Invalid file type: {file_extension}')

    # Flask checks that the 'Content-Length' header is present.
    # Otherwise, it rejects the request and returns a status code 400 - Bad Request.
    length_of_file = int(request.headers['CONTENT_LENGTH'])
    try:
        file_as_string = request.files['file'].read(length_of_file).decode()
    except UnicodeDecodeError:
        raise SlamdUnprocessableEntityException(message='Error while attempting to decode JSON file')

    DesignAssistantService.upload_da_session(file_as_string)

    # In the frontend, Javascript will reload the page automatically if it receives an OK response
    # Actual content of response does not matter
    return ''
