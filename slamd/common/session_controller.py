from flask import Blueprint, make_response

from slamd.common.session_service import SessionService

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('/save', methods=['GET'])
def save_session():
    json_string = SessionService.save_session()
    response = make_response(json_string.encode())
    response.headers['Content-Disposition'] = f'attachment; filename=session.json'
    response.mimetype = 'text/json'
    return response

