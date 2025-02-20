import json

import numpy as np
import pandas as pd
from werkzeug.datastructures import ImmutableMultiDict

from slamd.formulations.processing.forms.binder_selection_form import BinderSelectionForm
from slamd.formulations.processing.forms.concrete_selection_form import \
    ConcreteSelectionForm
from slamd.formulations.processing.forms.weights_form import WeightsForm
from slamd.formulations.processing.formulations_service import FormulationsService


def test_slamd_shows_concrete_formulations_page(client, monkeypatch):
    def mock_load_formulations_page(building_material):
        form = ConcreteSelectionForm()
        form.aggregates_selection.choices = [('Aggregates|uuid 1', 'Test Aggregate')]
        df = pd.DataFrame({'a': np.array([1, 2]), 'b': np.array([3, 4])})
        return form, df

    monkeypatch.setattr(FormulationsService, 'load_formulations_page', mock_load_formulations_page)

    response = client.get('/materials/formulations/concrete')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Concrete formulations' in html
    assert 'Binder formulations' not in html
    assert 'Powders' in html
    assert 'Aggregates (select one at least)' in html
    assert 'Liquids' in html
    assert 'Admixture' in html
    assert 'Custom' in html
    assert 'Processes' in html
    assert 'Constraint' in html
    assert 'Configure weights for each material type' in html

    assert '<th>a</th>' in html
    assert '<th>b</th>' in html
    assert '<td>1</td>' in html
    assert '<td>2</td>' in html
    assert '<td>3</td>' in html
    assert '<td>4</td>' in html

    assert 'Test Aggregate' in html


def test_slamd_shows_binder_formulations_page(client, monkeypatch):
    def mock_load_formulations_page(building_material):
        form = BinderSelectionForm()
        form.aggregates_selection.choices = [('Aggregates|uuid 1', 'Test Aggregate')]
        df = pd.DataFrame({'a': np.array([1, 2]), 'b': np.array([3, 4])})
        return form, df

    monkeypatch.setattr(FormulationsService, 'load_formulations_page', mock_load_formulations_page)

    response = client.get('/materials/formulations/binder')
    html = response.data.decode('utf-8')

    assert response.status_code == 200

    assert 'Concrete formulations' not in html
    assert 'Binder formulations' in html
    assert 'Powders' in html
    assert 'Aggregates (optional)' in html
    assert 'Liquids' in html
    assert 'Admixture' in html
    assert 'Custom' in html
    assert 'Processes' in html
    assert 'Constraint' in html
    assert 'Configure weights for each material type' in html

    assert '<th>a</th>' in html
    assert '<th>b</th>' in html
    assert '<td>1</td>' in html
    assert '<td>2</td>' in html
    assert '<td>3</td>' in html
    assert '<td>4</td>' in html

    assert 'Test Aggregate' in html


def test_slamd_adds_formulations_min_max_entries(client, monkeypatch):
    request = json.dumps(
        {
            "selected_materials": [
                {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Powder', 'name': 'Blended Powder 1-1'},
                {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Powder', 'name': 'Blended Powder 1-2'},
                {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Liquid', 'name': 'Blended Liquid 1-1'},
                {'uuid': '44bb60a4-22aa-11ed-92ba-2079188bdeea', 'type': 'Aggregates',
                 'name': 'Blended Aggregates 1-1'},
                {'uuid': 'fe6af2c7-22a8-11ed-8e81-2079188bdeea', 'type': 'Process', 'name': 'Process 1'}
            ],
            "selected_constraint_type": "Weight"
        }
    )
    response = client.post('/materials/formulations/concrete/add_min_max_entries', data=request)
    print(json.loads(response.data.decode('utf-8'))['template'])

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert 'process_entries-0-materials_entry_name' in template
    assert 'process_entries-0-increment' not in template
    assert 'process_entries-0-min' not in template
    assert 'process_entries-0-max' not in template
    assert 'Process 1' in template

    # liquid info entry
    assert 'liquid_info_entry' in template
    assert 'Liquids (Blended Liquid 1-1)' in template

    assert 'process_entries-1-materials_entry_name' not in template
    assert 'process_entries-1-increment' not in template
    assert 'process_entries-1-min' not in template
    assert 'process_entries-1-max' not in template

    assert 'materials_min_max_entries-0-materials_entry_name' in template
    assert 'materials_min_max_entries-0-increment' in template
    assert 'materials_min_max_entries-0-min' in template
    assert 'materials_min_max_entries-0-max' in template
    assert 'Powders (Blended Powder 1-1, Blended Powder 1-2)' in template

    assert 'materials_min_max_entries-1-materials_entry_name' in template
    assert 'materials_min_max_entries-1-increment' in template
    assert 'materials_min_max_entries-1-min' in template
    assert 'materials_min_max_entries-1-max' in template
    assert 'W/C Ratio' in template

    assert 'materials_min_max_entries-2-materials_entry_name' in template
    assert 'materials_min_max_entries-2-increment' in template
    assert 'materials_min_max_entries-2-min' in template
    assert 'materials_min_max_entries-2-max' in template
    assert 'Aggregates (Blended Aggregates 1-1)' in template

    assert 'materials_min_max_entries-3-materials_entry_name' not in template
    assert 'materials_min_max_entries-3-increment' not in template
    assert 'materials_min_max_entries-3-min' not in template
    assert 'materials_min_max_entries-3-max' not in template

    assert 'Create material formulations for given configuration' in template


def test_slamd_creates_formulation_batch(client, monkeypatch):
    def mock_create_materials_formulations(request_data, building_material):
        data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
        return pd.DataFrame.from_dict(data)

    monkeypatch.setattr(FormulationsService, 'create_materials_formulations', mock_create_materials_formulations)

    response = client.post('/materials/formulations/concrte/create_formulations_batch', data=b'{}')

    assert response.status_code == 200

    template = json.loads(response.data.decode('utf-8'))['template']
    assert '<table ' in template

    assert '<th>col_1</th>' in template
    assert '<th>col_2</th>' in template

    assert '<td>3</td>' in template
    assert '<td>a</td>' in template

    assert '<td>2</td>' in template
    assert '<td>b</td>' in template

    assert '<td>1</td>' in template
    assert '<td>c</td>' in template

    assert '<td>0</td>' in template
    assert '<td>d</td>' in template


def test_slamd_submits_dataset_after_creating_a_formulation(client, monkeypatch):
    mock_save_dataset_called_with = None

    def mock_save_dataset(request, building_material):
        nonlocal mock_save_dataset_called_with
        mock_save_dataset_called_with = request, building_material
        return None

    monkeypatch.setattr(FormulationsService, 'save_dataset', mock_save_dataset)

    response = client.post('/materials/formulations/concrete', data=b'{}')

    assert response.status_code == 302
    assert mock_save_dataset_called_with == (ImmutableMultiDict([]), 'concrete')
