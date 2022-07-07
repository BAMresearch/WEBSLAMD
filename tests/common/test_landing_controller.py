def test_slamd_loads(client):
    response = client.get("/", follow_redirects=True)

    assert b"SLAMD Dashboard" in response.data


def test_slamd_redirects_materials_page(client):
    response = client.get("/", follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/materials/base"
