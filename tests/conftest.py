import pytest
from flask_cors import CORS

from slamd import create_app


@pytest.fixture()
def app():
    app = create_app('testing', with_session=False)
    CORS(app)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
