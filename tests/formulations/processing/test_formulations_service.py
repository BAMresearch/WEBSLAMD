import numpy as np
import pandas as pd
import pytest
from werkzeug.datastructures import ImmutableMultiDict

from slamd import create_app
from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException
from slamd.discovery.processing.discovery_facade import DiscoveryFacade
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.building_materials_factory import BuildingMaterialsFactory
from slamd.formulations.processing.strategies.binder_strategy import BinderStrategy
from slamd.formulations.processing.formulations_service import FormulationsService
from slamd.materials.processing.materials_facade import MaterialsFacade, MaterialsForFormulations
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.models.process import Process
from tests.materials.materials_test_data import prepare_test_base_powders_for_blending, \
    prepare_test_base_liquids_for_blending, prepare_test_base_aggregates_for_blending, prepare_test_admixture

MATERIALS_CONFIG = [
    {'uuid': '1', 'type': 'Powder', 'min': 18.2, 'max': 40, 'increment': 0.1},
    {'uuid': '2', 'type': 'Liquid', 'min': 0.1, 'max': 0.9, 'increment': 0.01},
    {'uuid': '3', 'type': 'Aggregates', 'min': 67.6, 'max': 35, 'increment': None}
]

app = create_app('testing', with_session=False)


@pytest.mark.parametrize("context", ['concrete', 'binder'])
def test_load_formulations_page_loads_form_and_dataframe(monkeypatch, context):
    def mock_find_all():
        powder = Powder(name='test powder', type='powder')
        powder.uuid = '1'
        liquid1 = Liquid(name='test liquid 1', type='liquid')
        liquid1.uuid = '2'
        liquid2 = Liquid(name='test liquid 2', type='liquid')
        liquid2.uuid = '3'
        process = Process(name='test process', type='process')
        process.uuid = '4'
        return MaterialsForFormulations(powders=[powder],
                                        aggregates_list=[],
                                        liquids=[liquid1, liquid2],
                                        admixtures=[],
                                        customs=[],
                                        processes=[process])

    tmp_df = pd.DataFrame({'a': [1, 2], 'b': [2, 3]})

    def mock_query_dataset_by_name(filename):
        dataframe = tmp_df
        return Dataset(name=f'temporary_{context}.csv', dataframe=dataframe)

    monkeypatch.setattr(MaterialsFacade, 'find_all', mock_find_all)
    monkeypatch.setattr(DiscoveryFacade, 'query_dataset_by_name', mock_query_dataset_by_name)

    with app.test_request_context(f'/materials/formulations/{context}'):
        form, df = FormulationsService.load_formulations_page(context)

    assert form.powder_selection.choices == [('powder|1', 'test powder')]
    assert form.liquid_selection.choices == [('liquid|2', 'test liquid 1'), ('liquid|3', 'test liquid 2')]
    assert form.aggregates_selection.choices == []
    assert form.admixture_selection.choices == []
    assert form.custom_selection.choices == []
    assert form.process_selection.choices == [('process|4', 'test process')]

    assert df.to_dict() == tmp_df.to_dict()


def test_create_weights_form_computes_all_weights_for_concrete(monkeypatch):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context('/materials/formulations/concrete/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': [
                    {'uuid': '1', 'type': 'Powder', 'min': 18.2, 'max': 40, 'increment': 10.5},
                    {'uuid': '2', 'type': 'Liquid', 'min': 0.5, 'max': 0.6, 'increment': 0.1},
                    {'uuid': '3', 'type': 'Aggregates', 'min': 67.6, 'max': 35, 'increment': None}],
                'weight_constraint': '100'
            }

        form = FormulationsService.create_weights_form(weight_request_data, 'concrete')

        assert form.all_weights_entries.data == [{'idx': '0', 'weights': '18.2/9.1/72.7'},
                                                 {'idx': '1', 'weights': '18.2/10.92/70.88'},
                                                 {'idx': '2', 'weights': '28.7/14.35/56.95'},
                                                 {'idx': '3', 'weights': '28.7/17.22/54.08'},
                                                 {'idx': '4', 'weights': '39.2/19.6/41.2'},
                                                 {'idx': '5', 'weights': '39.2/23.52/37.28'}]


def test_create_weights_form_computes_all_weights_for_binder(monkeypatch):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context('/materials/formulations/binder/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': [
                    {'uuid': '1', 'type': 'Liquid', 'min': 0.2, 'max': 0.3, 'increment': 0.1},
                    {'uuid': '2', 'type': 'Aggregates', 'min': 20, 'max': 30, 'increment': 10},
                    {'uuid': '3', 'type': 'Powder', 'min': 66.67, 'max': 53.85, 'increment': None}],
                'weight_constraint': '100'
            }

        form = FormulationsService.create_weights_form(weight_request_data, 'binder')

        assert form.all_weights_entries.data == [{'idx': '0', 'weights': '13.33/20.0/66.67'},
                                                 {'idx': '1', 'weights': '11.67/30.0/58.33'},
                                                 {'idx': '2', 'weights': '18.46/20.0/61.54'},
                                                 {'idx': '3', 'weights': '16.16/30.0/53.85'}]


@pytest.mark.parametrize("context", ['concrete', 'binder'])
def test_create_weights_form_raises_exceptions_when_too_many_weights_are_requested(monkeypatch, context):
    monkeypatch.setattr(MaterialsFacade, 'get_material', _mock_get_material)

    with app.test_request_context(f'/materials/formulations/{context}/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': MATERIALS_CONFIG,
                'weight_constraint': '100'
            }

        with pytest.raises(SlamdRequestTooLargeException):
            FormulationsService.create_weights_form(weight_request_data, context)


@pytest.mark.parametrize("context", ['concrete', 'binder'])
def test_create_weights_form_raises_exceptions_when_weight_constraint_is_not_set(monkeypatch, context):
    with app.test_request_context(f'/materials/formulations/{context}/add_weights'):
        weight_request_data = \
            {
                'materials_formulation_configuration': MATERIALS_CONFIG,
                'weight_constraint': ''
            }

        with pytest.raises(ValueNotSupportedException):
            FormulationsService.create_weights_form(weight_request_data, context)


# noinspection PyUnresolvedReferences
def test_create_materials_formulations_creates_initial_formulation_batch_for_concrete(monkeypatch):
    mock_query_dataset_by_name_called_with = None
    mock_save_and_overwrite_dataset_called_with = None

    def mock_query_dataset_by_name(input):
        nonlocal mock_query_dataset_by_name_called_with
        mock_query_dataset_by_name_called_with = input
        return None

    def mock_get_process(uuid):
        return None

    def mock_get_material(material_type, uuid):
        if material_type == 'Powder':
            if uuid == 'additional':
                return _create_additional_powder()
            return prepare_test_base_powders_for_blending(material_type, uuid)
        elif material_type == 'Liquid':
            return prepare_test_base_liquids_for_blending(material_type, uuid)
        elif material_type == 'Aggregates':
            return prepare_test_base_aggregates_for_blending(material_type, uuid)
        elif material_type == 'Admixture':
            return prepare_test_admixture()
        return None

    def mock_save_and_overwrite_dataset(input, filename):
        nonlocal mock_save_and_overwrite_dataset_called_with
        mock_save_and_overwrite_dataset_called_with = input, filename
        return None

    monkeypatch.setattr(DiscoveryFacade, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(MaterialsFacade, 'get_material', mock_get_material)
    monkeypatch.setattr(MaterialsFacade, 'get_process', mock_get_process)
    monkeypatch.setattr(DiscoveryFacade, 'save_and_overwrite_dataset', mock_save_and_overwrite_dataset)

    formulations_data = {
        'materials_request_data': {
            'materials_formulation_configuration': [
                {'uuids': 'uuid1,additional', 'type': 'Powder'},
                {'uuids': 'uuid2', 'type': 'Liquid'},
                {'uuids': 'uuid admixture', 'type': 'Admixture'},
                {'uuids': 'uuid3', 'type': 'Aggregates'}]
        },
        'weights_request_data': {
            'all_weights': ['200.0/20.0/1.0/779.0', '200.0/30.0/1.0/769.0', '300.0/20.0/2.0/678.0',
                            '300.0/30.0/2.0/668.0']
        },
        'processes_request_data': {
            'processes': []
        },
        'sampling_size': 1
    }

    expected_df = _create_expected_df_as_dict()

    df = FormulationsService.create_materials_formulations(formulations_data, 'concrete')

    assert df.replace({np.nan: None}).to_dict() == expected_df
    assert mock_query_dataset_by_name_called_with == 'temporary_concrete.csv'
    assert mock_save_and_overwrite_dataset_called_with[0].name == 'temporary_concrete.csv'
    assert mock_save_and_overwrite_dataset_called_with[1] == 'temporary_concrete.csv'


# As we already tested details of the creation of a batch for concrete we choose to only check the basic data flow here
def test_create_materials_formulations_creates_initial_formulation_batch_for_binder(monkeypatch):
    mock_create_building_material_strategy_called_with = None
    mock_create_formulation_batch_called_with = None

    def mock_create_building_material_strategy(building_material):
        nonlocal mock_create_building_material_strategy_called_with
        mock_create_building_material_strategy_called_with = building_material
        return BinderStrategy

    def mock_create_formulation_batch(request_data):
        nonlocal mock_create_formulation_batch_called_with
        mock_create_formulation_batch_called_with = 'dummy formulations request data'
        return 'batch'

    monkeypatch.setattr(BuildingMaterialsFactory, 'create_building_material_strategy',
                        mock_create_building_material_strategy)
    monkeypatch.setattr(BinderStrategy, 'create_formulation_batch', mock_create_formulation_batch)

    batch = FormulationsService.create_materials_formulations('dummy formulations request data', 'binder')

    assert mock_create_building_material_strategy_called_with == 'binder'
    assert mock_create_formulation_batch_called_with == 'dummy formulations request data'
    assert batch == 'batch'


@pytest.mark.parametrize("context", ['concrete', 'binder'])
def test_delete_formulation_deletes_tempary_dataset(monkeypatch, context):
    mock_delete_dataset_by_name_called_with = None

    def mock_delete_dataset_by_name(input):
        nonlocal mock_delete_dataset_by_name_called_with
        mock_delete_dataset_by_name_called_with = input
        return None

    monkeypatch.setattr(DiscoveryFacade, 'delete_dataset_by_name', mock_delete_dataset_by_name)

    FormulationsService.delete_formulation(context)

    assert mock_delete_dataset_by_name_called_with == f'temporary_{context}.csv'


@pytest.mark.parametrize("context", ['concrete', 'binder'])
def test_save_dataset_deletes_temporary_and_creates_dataset_with_custom_name(monkeypatch, context):
    mock_delete_dataset_by_name_called_with = None
    mock_query_dataset_by_name_called_with = None
    mock_save_dataset_called_with = None

    def mock_query_dataset_by_name(input):
        nonlocal mock_query_dataset_by_name_called_with
        mock_query_dataset_by_name_called_with = input
        return Dataset()

    def mock_delete_dataset_by_name(input):
        nonlocal mock_delete_dataset_by_name_called_with
        mock_delete_dataset_by_name_called_with = input
        return None

    def mock_save_dataset(input):
        nonlocal mock_save_dataset_called_with
        mock_save_dataset_called_with = input
        return None

    monkeypatch.setattr(DiscoveryFacade, 'delete_dataset_by_name', mock_delete_dataset_by_name)
    monkeypatch.setattr(DiscoveryFacade, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(DiscoveryFacade, 'save_dataset', mock_save_dataset)

    form = ImmutableMultiDict([('dataset_name', 'dataset_name')])

    FormulationsService.save_dataset(form, context)

    assert mock_query_dataset_by_name_called_with == f'temporary_{context}.csv'
    assert mock_delete_dataset_by_name_called_with == f'temporary_{context}.csv'
    assert mock_save_dataset_called_with.name == 'dataset_name.csv'


def _create_additional_powder():
    powder = Powder(name='powder 1', type='Powder',
                    costs=Costs(co2_footprint=2, costs=2.2, delivery_time=12),
                    composition=Composition(fe3_o2=2.3),
                    structure=Structure(fine=1, gravity=2),
                    additional_properties=[])
    powder.uuid = 'additional'
    return powder


def _create_expected_df_as_dict():
    return {'Idx_Sample': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7},
            'Powder (kg)': {0: 200.0, 1: 200.0, 2: 300.0, 3: 300.0, 4: 200.0, 5: 200.0, 6: 300.0, 7: 300.0},
            'Liquid (kg)': {0: 20.0, 1: 30.0, 2: 20.0, 3: 30.0, 4: 20.0, 5: 30.0, 6: 20.0, 7: 30.0},
            'Admixture (kg)': {0: 1.0, 1: 1.0, 2: 2.0, 3: 2.0, 4: 1.0, 5: 1.0, 6: 2.0, 7: 2.0},
            'Aggregates (kg)': {0: 779.0, 1: 769.0, 2: 678.0, 3: 668.0, 4: 779.0, 5: 769.0, 6: 678.0, 7: 668.0},
            'Materials': {0: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          1: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          2: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          3: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          4: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          5: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          6: 'powder 1, liquid 2, admixture 1, aggregate 3',
                          7: 'powder 1, liquid 2, admixture 1, aggregate 3'},
            'Prop1': {0: 5.0, 1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0},
            'Prop2': {0: 'Other Category', 1: 'Other Category', 2: 'Other Category', 3: 'Other Category',
                      4: 'Other Category', 5: 'Other Category', 6: 'Other Category', 7: 'Other Category'},
            'Prop3': {0: 'Not a number 2', 1: 'Not a number 2', 2: 'Not a number 2', 3: 'Not a number 2',
                      4: 'Not a number 2', 5: 'Not a number 2', 6: 'Not a number 2', 7: 'Not a number 2'},
            'Prop4': {0: 12.0, 1: 12.0, 2: 12.0, 3: 12.0, 4: None, 5: None, 6: None, 7: None},
            'fe3_o2': {0: 10.0, 1: 10.0, 2: 10.0, 3: 10.0, 4: 2.3, 5: 2.3, 6: 2.3, 7: 2.3},
            'al2_o3': {0: 7.0, 1: 7.0, 2: 7.0, 3: 7.0, 4: None, 5: None, 6: None, 7: None},
            'fine': {0: 50.0, 1: 50.0, 2: 50.0, 3: 50.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0},
            'gravity': {0: 6.0, 1: 6.0, 2: 6.0, 3: 6.0, 4: 6.0, 5: 6.0, 6: 6.0, 7: 6.0},
            'na2_si_o3': {0: 20.0, 1: 20.0, 2: 20.0, 3: 20.0, 4: 20.0, 5: 20.0, 6: 20.0, 7: 20.0},
            'na2_si_o3_mol': {0: 4.0, 1: 4.0, 2: 4.0, 3: 4.0, 4: 4.0, 5: 4.0, 6: 4.0, 7: 4.0},
            'na_o_h': {0: 4.1, 1: 4.1, 2: 4.1, 3: 4.1, 4: 4.1, 5: 4.1, 6: 4.1, 7: 4.1},
            'h2_o_mol': {0: 11.0, 1: 11.0, 2: 11.0, 3: 11.0, 4: 11.0, 5: 11.0, 6: 11.0, 7: 11.0},
            'fine_aggregates': {0: 27.0, 1: 27.0, 2: 27.0, 3: 27.0, 4: 27.0, 5: 27.0, 6: 27.0, 7: 27.0},
            'coarse_aggregates': {0: 9.0, 1: 9.0, 2: 9.0, 3: 9.0, 4: 9.0, 5: 9.0, 6: 9.0, 7: 9.0},
            'bulk_density': {0: 16.0, 1: 16.0, 2: 16.0, 3: 16.0, 4: 16.0, 5: 16.0, 6: 16.0, 7: 16.0},
            'fineness_modulus': {0: 5.0, 1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0},
            'water_absorption': {0: 10.0, 1: 10.0, 2: 10.0, 3: 10.0, 4: 10.0, 5: 10.0, 6: 10.0, 7: 10.0},
            'total costs / ton': {0: 26.23, 1: 26.34, 2: 29.27, 3: 29.37, 4: 16.68, 5: 16.77, 6: 14.93, 7: 15.03},
            'total co2_footprint / ton': {0: 58.74, 1: 58.14, 2: 53.68, 3: 53.08, 4: 55.14, 5: 54.54, 6: 48.28,
                                          7: 47.68},
            'total delivery_time ': {0: 40.0, 1: 40.0, 2: 40.0, 3: 40.0, 4: 40.0, 5: 40.0, 6: 40.0, 7: 40.0}}


# noinspection PyTypeChecker
# mock uuid so we do simply use strings instead of actual uuids
def _mock_get_material(material_type, uuid):
    if material_type == 'Powder':
        if uuid == '1':
            powder = Powder(name='test blended powder', type='powder', is_blended=True, blending_ratios='0.2/0.8',
                            created_from=['4', '5'])
            powder.uuid = '1'
            return powder
        elif uuid == '4':
            powder = Powder(name='test powder 1', type='powder')
            powder.uuid = '4'
            return powder
        else:
            powder = Powder(name='test powder 2', type='powder')
            powder.uuid = '5'
            return powder
    elif material_type == 'Aggregates' and uuid == '2':
        aggregates = Aggregates(name='test aggregate', type='aggregates')
        aggregates.uuid = '2'
        return aggregates
    else:
        custom = Custom(name='test custom', type='custom')
        custom.uuid = '3'
        return custom
