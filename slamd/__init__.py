from flask import Flask
from flask_cors import CORS

import config
from slamd.common.error_handling import handle_404, handle_400
from slamd.common.landing_controller import landing
from slamd.materials.materials_controller import materials


def create_app(env=None):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.get_config_obj(env))

    app.register_blueprint(landing)
    app.register_blueprint(materials)

    app.register_error_handler(404, lambda err: handle_404(err))
    app.register_error_handler(400, lambda err: handle_400(err))
    return app
