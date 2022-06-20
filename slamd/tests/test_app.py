import pytest

import config
from slamd import app as slamd


@pytest.fixture()
def app():
    slamd.config.from_object(config.ConfigTesting)

    yield slamd


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_slamd_loads(client):
    response = client.get("/", follow_redirects=True)

    assert b"SLAMD Dashboard" in response.data


def test_slamd_redirects_materials_page(client):
    response = client.get("/", follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/materials"
