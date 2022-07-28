from slamd import create_app
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.models.dataset import Dataset


def test_slamd_shows_discovery_page(client, monkeypatch):
    def mock_list_datasets():
        return [Dataset('first dataset'), Dataset('second dataset')]

    monkeypatch.setattr(DiscoveryService, 'list_datasets', mock_list_datasets)

    response = client.get('/materials/discovery')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Material Discovery' in html
    assert 'CSV File Upload' in html

    assert 'All datasets' in html
    assert 'first dataset' in html
    assert 'second dataset' in html


def test_slamd_creates_new_dataset_when_saving_is_successful(client, monkeypatch):
    app = create_app('testing', with_session=False)

    def mock_save_dataset(submitted_form, submitted_file):
        return (True, None)

    with app.test_request_context('/materials/discovery'):
        monkeypatch.setattr(DiscoveryService, 'save_dataset', mock_save_dataset)
        form = UploadDatasetForm(dataset='test dataset')

        response = client.post('/materials/discovery', data=form.data)

    assert response.status_code == 302
    assert b'test dataset' not in response.data
    assert response.request.path == '/materials/discovery'
