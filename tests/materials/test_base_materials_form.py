def test_slamd_base_materials_form_contains_costs(client):
    response = client.get("/materials")

    assert response.status_code == 200
    assert b'CO2-Footprint' in response.data
    assert b'Costs' in response.data
    assert b'Delivery time' in response.data
