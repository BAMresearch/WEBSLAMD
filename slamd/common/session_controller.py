from flask import Blueprint, make_response, request

from slamd.common.session_service import SessionService

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('/save', methods=['GET'])
def save_session():
    json_string = SessionService.save_session()
    response = make_response(json_string.encode())
    response.headers['Content-Disposition'] = f'attachment; filename=session.json'
    response.mimetype = 'text/json'
    return response


@session_bp.route('/restore', methods=['POST'])
def restore_session():
    length_of_file = int(request.headers['CONTENT_LENGTH'])
    file_as_string = request.files['file'].read(length_of_file).decode()
    SessionService.load_session(file_as_string)
    return ""

