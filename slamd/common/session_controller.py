from flask import Blueprint, render_template

session = Blueprint('session', __name__, url_prefix='/session')


@session.route('/save', methods=['GET'])
def save_session():
    pass
