from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_wtf import CSRFProtect

import config
from slamd.common.error_handling import handle_404, handle_400
from slamd.common.landing_controller import landing
from slamd.materials.processing.base_materials_controller import base_materials


def create_app(env=None, with_session=True):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.get_config_obj(env))

    if with_session:
        Session(app)
        csrf = CSRFProtect(app)
        csrf.init_app(app)

    app.register_blueprint(landing)
    app.register_blueprint(base_materials)

    app.register_error_handler(404, lambda err: handle_404(err))
    app.register_error_handler(400, lambda err: handle_400(err))
    return app
