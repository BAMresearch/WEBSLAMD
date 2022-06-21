import pytest
from flask_cors import CORS

import config
from slamd import app as slamd


@pytest.fixture()
def app():
    slamd.config.from_object(config.ConfigTesting)
    CORS(slamd)

    yield slamd


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
