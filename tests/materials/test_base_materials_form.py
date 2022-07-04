def test_slamd_base_materials_form_contains_costs(client):
    response = client.get('/materials')

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Material type' in response.data
    assert bytes('CO₂ footprint', 'utf-8') in response.data
    assert b'Costs' in response.data
    assert b'Delivery time' in response.data
