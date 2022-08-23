import json

from slamd.formulations.processing.forms.materials_and_processes_selection_form import \
    MaterialsAndProcessesSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_service import FormulationsService


def test_slamd_shows_formulations_page(client, monkeypatch):
    def mock_populate_selection_form():
        form = MaterialsAndProcessesSelectionForm()
        form.aggregates_selection.choices = [('Aggregates|uuid 1', 'Test Aggregate')]
        return form

    monkeypatch.setattr(FormulationsService, 'populate_selection_form', mock_populate_selection_form)

    response = client.get('/materials/formulations')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Materials Formulations' in html
    assert 'Powders' in html
    assert 'Aggregates' in html
    assert 'Liquids' in html
    assert 'Admixture' in html
    assert 'Custom' in html
    assert 'Processes' in html
    assert 'Constraint' in html
    assert 'Confirm Selection' in html

    assert 'Test Aggregate' in html


def test_slamd_adds_formulations_min_max_entries(client, monkeypatch):
    request = json.dumps(
        [
            {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Powder', 'name': 'Blended Powder 1-1'},
            {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Powder', 'name': 'Blended Powder 1-2'},
            {'uuid': 'fe6af2c7-22a8-11ed-8e81-2079188bdeea', 'type': 'Process', 'name': 'Process 1'}
        ]
    )

    response = client.post('/materials/formulations/add_min_max_entries', data=request)

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'non_editable_entries-0-materials_entry_name' in template
    assert 'non_editable_entries-0-increment' not in template
    assert 'non_editable_entries-0-min' not in template
    assert 'non_editable_entries-0-max' not in template

    assert 'non_editable_entries-1-materials_entry_name' not in template
    assert 'non_editable_entries-1-increment' not in template
    assert 'non_editable_entries-1-min' not in template
    assert 'non_editable_entries-1-max' not in template

    assert 'materials_min_max_entries-0-materials_entry_name' in template
    assert 'materials_min_max_entries-0-increment' in template
    assert 'materials_min_max_entries-0-min' in template
    assert 'materials_min_max_entries-0-max' in template

    assert 'materials_min_max_entries-1-materials_entry_name' in template
    assert 'materials_min_max_entries-1-increment' in template
    assert 'materials_min_max_entries-1-min' in template
    assert 'materials_min_max_entries-1-max' in template

    assert 'Show mixture in terms of base material composition' in template


def test_slamd_shows_weights_of_formulations(client, monkeypatch):
    def mock_create_weights_form(data):
        form = WeightsForm()
        entry1 = form.all_weights_entries.append_entry()
        entry1.idx.data = '0'
        entry1.weights.data = ['15 | 2.25/7,75']
        entry2 = form.all_weights_entries.append_entry()
        entry2.idx.data = '1'
        entry2.weights.data = ['10 | 5/10']
        return form, 'Powder | Liquid 1/Liquid 2'

    monkeypatch.setattr(FormulationsService, 'create_weights_form', mock_create_weights_form)

    # We mock processing of the request body, so it does not matter which data we pass. The simplest option is empty
    response = client.post('/materials/formulations/add_weights', data=b'{}')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'Weights in terms of the original base materials.' in template
    assert 'Powder | Liquid 1/Liquid 2' in template
    assert 'all_weights_entries-0-weights' in template
    assert 'all_weights_entries-1-weights' in template
    assert '15 | 2.25/7,75' in template
    assert '10 | 5/10' in template
