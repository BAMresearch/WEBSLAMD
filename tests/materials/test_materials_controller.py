def test_slamd_selects_powder(client):
    response = client.get("/materials/powder")

    assert response.status_code == 200
    assert 'Fe2O3' in response.json['template']
    assert 'SiO2' in response.json['template']
    assert 'Al2O3' in response.json['template']
    assert 'CaO' in response.json['template']
    assert 'MgO' in response.json['template']
    assert 'Na2O' in response.json['template']
    assert 'K2O' in response.json['template']
    assert 'SO3' in response.json['template']
    assert 'TiO2' in response.json['template']
    assert 'P2O5' in response.json['template']
    assert 'SrO' in response.json['template']
    assert 'Mn2O3' in response.json['template']


def test_slamd_selects_liquid(client):
    response = client.get("/materials/liquid")

    assert response.status_code == 200
    assert 'Na2SiO3' in response.json['template']
    assert 'NaOH' in response.json['template']
    assert 'Na2SiO3 specific' in response.json['template']
    assert 'NaOH specific' in response.json['template']
    assert 'Total solution' in response.json['template']
    assert 'Na2O (I)' in response.json['template']
    assert 'SiO2 (I)' in response.json['template']
    assert 'H2O' in response.json['template']
    assert 'Na2O (dry) (%m)' in response.json['template']
    assert 'SiO2 (dry) (%m)' in response.json['template']
    assert 'Water (%m)' in response.json['template']
    assert 'Total NaOH (%m)' in response.json['template']


def test_slamd_selects_aggregates(client):
    response = client.get("/materials/aggregates")

    assert response.status_code == 200
    template = response.json['template']
    assert 'Fine Aggregates' in template
    assert 'Coarse Aggregates' in template
    assert 'Type' in template
    assert 'Grading Curve' in template


def test_slamd_selects_admixture(client):
    response = client.get("/materials/admixture")

    assert response.status_code == 200
    template = response.json['template']
    assert 'Composition' in template
    assert 'Type' in template


def test_slamd_selects_process(client):
    response = client.get("/materials/process")

    template = response.json['template']
    assert response.status_code == 200
    assert 'Duration' in template
    assert 'Temperature' in template
    assert 'Relative Humidity' in template
