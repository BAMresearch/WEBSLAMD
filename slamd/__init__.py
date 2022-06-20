import os

from flask import Flask, redirect, render_template

import config
from slamd.materials.materials_controller import materials

app = Flask(__name__)
app.config.from_object(config.get_config_obj(os.getenv('FLASK_ENV')))


@app.route('/', methods=['GET'])
def landing():
    return redirect('/materials')


@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


app.register_blueprint(materials)
