from flask import Blueprint, render_template

landing = Blueprint('landing', __name__)


@landing.route('/', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')
