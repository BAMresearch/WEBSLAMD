def test_slamd_selects_powder(client):
    response = client.get("/materials/powder")

    assert response.status_code == 200
    assert 'FeO' in response.json['template']


def test_slamd_selects_liquid(client):
    response = client.get("/materials/liquid")

    assert response.status_code == 200
    assert 'Precursor' in response.json['template']


def test_slamd_selects_aggregates(client):
    response = client.get("/materials/aggregates")

    assert response.status_code == 200
    assert 'Fine Aggregates' in response.json['template']
    assert 'Coarse Aggregates' in response.json['template']
    assert 'Type' in response.json['template']
    assert 'Grading Curve' in response.json['template']
