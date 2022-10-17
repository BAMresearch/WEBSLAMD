from flask import Blueprint, make_response, request, redirect, url_for

from slamd.common.session_service import SessionService

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('/save', methods=['GET'])
def save_session():
    json_string = SessionService.convert_session_to_json_string()
    response = make_response(json_string.encode())
    response.headers['Content-Disposition'] = f'attachment; filename=session.json'
    response.mimetype = 'text/json'
    return response


@session_bp.route('/restore', methods=['POST'])
def restore_session():
    length_of_file = int(request.headers['CONTENT_LENGTH'])
    file_as_string = request.files['file'].read(length_of_file).decode()
    SessionService.load_session_from_json_string(file_as_string)
    return ''


@session_bp.route('/clear', methods=['GET'])
def clear_session():
    SessionService.clear_session()
    return redirect(request.referrer)

