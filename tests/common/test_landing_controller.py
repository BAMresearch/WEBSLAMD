def test_slamd_loads(client):
    response = client.get("/", follow_redirects=True)

    assert b"SLAMD Dashboard" in response.data


def test_slamd_shows_404_page(client):
    response = client.get("/a_completely_invalid_page", follow_redirects=True)

    assert response.status_code == 404
    assert b'Not found' in response.data


def test_slamd_redirects_materials_page(client):
    response = client.get("/", follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/materials/base"
