from flask import Flask, render_template
from flask_cors import CORS

import config
from slamd.common.landing_controller import landing
from slamd.materials.materials_controller import materials


def handle_404(err):
    return render_template('404.html')


def handle_400(err):
    return render_template('400.html')


def create_app(env=None):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.get_config_obj(env))

    app.register_blueprint(landing)
    app.register_blueprint(materials)

    app.register_error_handler(404, lambda err: handle_404(err))
    app.register_error_handler(400, lambda err: handle_400(err))
    return app
