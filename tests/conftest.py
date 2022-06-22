import pytest
from flask_cors import CORS

from slamd import create_app


@pytest.fixture()
def app():
    app = create_app('testing')
    CORS(app)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

