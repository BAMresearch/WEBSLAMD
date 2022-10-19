def test_slamd_shows_404_page(client):
    response = client.get('/a_completely_invalid_page', follow_redirects=True)

    assert response.status_code == 404
    assert b'Resource not found: The requested page is not available' in response.data
