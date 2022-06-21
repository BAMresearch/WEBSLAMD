import os

from flask import Flask, redirect, render_template
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

import config
from slamd.materials.materials_controller import materials

app = Flask(__name__)
CORS(app)
app.config.from_object(config.get_config_obj(os.getenv('FLASK_ENV')))


@app.route('/', methods=['GET'])
def landing():
    return redirect('/materials')


@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


@app.errorhandler(BadRequest)
def handle_400(err):
    return render_template('400.html'), 400


app.register_blueprint(materials)
