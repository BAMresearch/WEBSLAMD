from flask import Blueprint, make_response, request, redirect

from slamd.common.error_handling import SlamdUnprocessableEntityException, ValueNotSupportedException
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
def load_session():
    if 'file' not in request.files:
        raise SlamdUnprocessableEntityException(message='Request did not contain a file')

    file_ending = request.files['file'].filename.lower().split('.')[-1]
    if file_ending != 'json':
        raise ValueNotSupportedException(message=f'Invalid file type: {file_ending}')

    length_of_file = int(request.headers['CONTENT_LENGTH'])
    try:
        file_as_string = request.files['file'].read(length_of_file).decode()
    except UnicodeDecodeError:
        raise SlamdUnprocessableEntityException(message='Error while attempting to decode JSON file')

    SessionService.load_session_from_json_string(file_as_string)

    # In the frontend, Javascript will reload the page automatically if it receives an OK response
    # Actual content of response does not matter
    # Return empty string, OK is attached automatically
    return ''


@session_bp.route('/clear', methods=['GET'])
def clear_session():
    SessionService.clear_session()
    return redirect(request.referrer)

