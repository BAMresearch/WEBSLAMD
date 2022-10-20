from flask import Blueprint, make_response, request

from slamd.common.error_handling import SlamdUnprocessableEntityException, ValueNotSupportedException
from slamd.common.session_backup.session_service import SessionService

session_blueprint = Blueprint('session', __name__, url_prefix='/session')

"""
    The form that serves these endpoints is found in the navbar. As such it is not created using WTForms.
    It relies on CSRF token elements in the body of the page for authentication.
    These are usually provided by other WTForms. However, some pages may not have form elements on them, in particular
    the landing page.
    These pages require the manual addition of CSRF token fields.
"""


@session_blueprint.route('/', methods=['GET'])
def save_session():
    json_string = SessionService.convert_session_to_json_string()
    response = make_response(json_string.encode())
    filename = SessionService.create_default_filename()
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.mimetype = 'text/json'
    return response


@session_blueprint.route('/', methods=['POST'])
def load_session():
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

    SessionService.load_session_from_json_string(file_as_string)

    # In the frontend, Javascript will reload the page automatically if it receives an OK response
    # Actual content of response does not matter
    return ''


@session_blueprint.route('/', methods=['DELETE'])
def clear_session():
    SessionService.clear_session()

    # In the frontend, Javascript will reload the page automatically if it receives an OK response
    # Actual content of response does not matter
    return ''
