from slamd import create_app
from slamd.formulations.processing.strategies.binder_strategy import BinderStrategy


"""
Most of the logic is already tested within test_formulations_service. Thus, we only test the functions which are not
yet properly covered in here.
"""


def test_create_min_max_form(monkeypatch):
    formulation_selection = [
        {'uuid': '1', 'type': 'Powder', 'name': 'Blended Powder-0.3/0.7'},
        {'uuid': '2', 'type': 'Powder', 'name': 'Blended Powder-0.5/0.5'},
        {'uuid': '3', 'type': 'Liquid', 'name': 'Chemical'},
        {'uuid': '4', 'type': 'Liquid', 'name': 'Water'},
        {'uuid': '5', 'type': 'Admixture', 'name': 'Admixture 1'},
        {'uuid': '6', 'type': 'Process', 'name': 'Heating'}]

    expected_materials_min_max_entries = [{'uuid_field': '3,4',
                                           'type_field': 'Liquid',
                                           'materials_entry_name': 'W/C Ratio',
                                           'increment': None,
                                           'min': None,
                                           'max': None},
                                          {'uuid_field': '5',
                                           'type_field': 'Admixture',
                                           'materials_entry_name': 'Admixtures (Admixture 1)',
                                           'increment': None,
                                           'min': None,
                                           'max': None},
                                          {'uuid_field': '1,2',
                                           'type_field': 'Powder',
                                           'materials_entry_name': 'Powders (Blended Powder-0.3/0.7, '
                                                                   'Blended Powder-0.5/0.5)',
                                           'increment': None,
                                           'min': None,
                                           'max': None}]

    expected_process_entries = [{'uuid_field': '6',
                                 'type_field': 'Process',
                                 'materials_entry_name': 'Heating'}]

    expected_liquid_entry = 'Liquids (Chemical, Water)'

    app = create_app('testing', with_session=False)
    with app.test_request_context('/materials/formulations/binder'):
        result = BinderStrategy.create_min_max_form(formulation_selection)

    assert result.data['materials_min_max_entries'] == expected_materials_min_max_entries
    assert result.data['process_entries'] == expected_process_entries
    assert result.data['liquid_info_entry'] == expected_liquid_entry
