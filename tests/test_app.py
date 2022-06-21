def test_slamd_loads(client):
    response = client.get("/", follow_redirects=True)

    assert b"SLAMD Dashboard" in response.data


def test_slamd_redirects_materials_page(client):
    response = client.get("/", follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/materials"


def test_slamd_selects_type(client):
    response = client.get("/materials/liquid")
    print(str(response))
    assert response.status_code == 200
    assert 'Precursor' in response.json['template']
