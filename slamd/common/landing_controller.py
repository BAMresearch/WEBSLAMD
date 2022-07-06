from flask import Blueprint, redirect

landing = Blueprint('landing', __name__)


@landing.route('/', methods=['GET'])
def landing_page():
    return redirect('/materials/base')
