import pandas as pd
import pytest
from werkzeug.datastructures import ImmutableMultiDict

from slamd import create_app
from slamd.discovery.processing.discovery_facade import DiscoveryFacade
from slamd.discovery.processing.models.dataset import Dataset
from slamd.formulations.processing.formulations_service import FormulationsService
from slamd.formulations.processing.strategies.building_material_strategy import BuildingMaterialStrategy
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
        if material_type.lower() == 'powder':
            if uuid == 'additional':
                return _create_additional_powder()
            return prepare_test_base_powders_for_blending(material_type, uuid)
        elif material_type.lower() == 'liquid':
            return prepare_test_base_liquids_for_blending(material_type, uuid)
        elif material_type.lower() == 'aggregates':
            return prepare_test_base_aggregates_for_blending(material_type, uuid)
        elif material_type.lower() == 'admixture':
            return prepare_test_admixture()
        return None

    def mock_save_and_overwrite_dataset(input, filename):
        nonlocal mock_save_and_overwrite_dataset_called_with
        mock_save_and_overwrite_dataset_called_with = input, filename
        return None

    def mock_get_specific_gravities(materials_dict):
        return {
            "uuid1": 1,
            "additional": 2,
            "uuid2": 3,
            "uuid admixture": 4,
            "uuid3": 5,
        }

    monkeypatch.setattr(DiscoveryFacade, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(MaterialsFacade, 'get_material', mock_get_material)
    monkeypatch.setattr(MaterialsFacade, 'get_process', mock_get_process)
    monkeypatch.setattr(DiscoveryFacade, 'save_and_overwrite_dataset', mock_save_and_overwrite_dataset)
    monkeypatch.setattr(BuildingMaterialStrategy, '_get_specific_gravities', mock_get_specific_gravities)

    formulations_data = {
        'materials_request_data': {
            'min_max_data': [
                {'uuid': 'uuid1,additional', 'type': 'Powder', 'increment': 50, 'min': 350, 'max': 400},
                {'uuid': 'uuid2', 'type': 'Liquid', 'increment': 5, 'min': 35, 'max': 40},
                {'uuid': 'uuid admixture', 'type': 'Admixture', 'increment': 1, 'min': 2, 'max': 3},
                {'uuid': 'uuid3', 'type': 'Aggregates', 'increment': None, 'min': None, 'max': None}]
        },
        'constraint': 1.00,
        'selected_constraint_type': 'Volume',
        'processes_request_data': {
            'processes': []
        },
        'sampling_size': 1
    }

    expected_df = _create_expected_concrete_df()

    df = FormulationsService.create_materials_formulations(formulations_data, 'concrete')

    assert df.equals(expected_df)
    assert mock_query_dataset_by_name_called_with == 'temporary_concrete.csv'
    assert mock_save_and_overwrite_dataset_called_with[0].name == 'temporary_concrete.csv'
    assert mock_save_and_overwrite_dataset_called_with[1] == 'temporary_concrete.csv'


# noinspection PyUnresolvedReferences
def test_create_materials_formulations_creates_initial_formulation_batch_for_binder(monkeypatch):
    mock_query_dataset_by_name_called_with = None
    mock_save_and_overwrite_dataset_called_with = None

    def mock_query_dataset_by_name(input):
        nonlocal mock_query_dataset_by_name_called_with
        mock_query_dataset_by_name_called_with = input
        return None

    def mock_get_process(uuid):
        return None

    def mock_get_material(material_type, uuid):
        if material_type.lower() == 'powder':
            return prepare_test_base_powders_for_blending(material_type, uuid)
        elif material_type.lower() == 'liquid':
            return prepare_test_base_liquids_for_blending(material_type, uuid)
        elif material_type.lower() == 'aggregates':
            return prepare_test_base_aggregates_for_blending(material_type, uuid)
        elif material_type.lower() == 'admixture':
            return prepare_test_admixture()
        return None

    def mock_save_and_overwrite_dataset(input, filename):
        nonlocal mock_save_and_overwrite_dataset_called_with
        mock_save_and_overwrite_dataset_called_with = input, filename
        return None

    def mock_get_specific_gravities(materials_dict):
        return {
            "uuid1": 1,
            "additional": 2,
            "uuid2": 3,
            "uuid admixture": 4,
            "uuid3": 5,
        }

    monkeypatch.setattr(DiscoveryFacade, 'query_dataset_by_name', mock_query_dataset_by_name)
    monkeypatch.setattr(MaterialsFacade, 'get_material', mock_get_material)
    monkeypatch.setattr(MaterialsFacade, 'get_process', mock_get_process)
    monkeypatch.setattr(DiscoveryFacade, 'save_and_overwrite_dataset', mock_save_and_overwrite_dataset)
    monkeypatch.setattr(BuildingMaterialStrategy, '_get_specific_gravities', mock_get_specific_gravities)

    formulations_data = {
        'materials_request_data': {
            'min_max_data': [
                {'uuid': 'uuid1', 'type': 'Aggregates', 'increment': 50, 'min': 350, 'max': 400},
                {'uuid': 'uuid2', 'type': 'Liquid', 'increment': 5, 'min': 35, 'max': 40},
                {'uuid': 'uuid admixture', 'type': 'Admixture', 'increment': 1, 'min': 2, 'max': 3},
                {'uuid': 'uuid3', 'type': 'Powder', 'increment': None, 'min': None, 'max': None}]
        },
        'constraint': 500,
        'selected_constraint_type': 'Weight',
        'processes_request_data': {
            'processes': []
        },
        'sampling_size': 1
    }

    expected_df = _create_expected_binder_df()

    df = FormulationsService.create_materials_formulations(formulations_data, 'binder')

    with open("temp.json", "w") as f:
        import json
        json.dump(df.to_dict(orient="list"), f)

    assert df.equals(expected_df)
    assert mock_query_dataset_by_name_called_with == 'temporary_binder.csv'
    assert mock_save_and_overwrite_dataset_called_with[0].name == 'temporary_binder.csv'
    assert mock_save_and_overwrite_dataset_called_with[1] == 'temporary_binder.csv'


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
                    structure=Structure(fine=1),
                    additional_properties=[])
    powder.uuid = 'additional'
    return powder


def _create_expected_concrete_df():
    return pd.DataFrame({"Idx_Sample": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                         "Powder (kg)": [350.0, 350.0, 350.0, 350.0, 400.0, 400.0, 400.0, 400.0, 350.0, 350.0, 350.0,
                                         350.0, 400.0, 400.0, 400.0, 400.0],
                         "Liquid (kg)": [122.5, 122.5, 140.0, 140.0, 140.0, 140.0, 160.0, 160.0, 122.5, 122.5, 140.0,
                                         140.0, 140.0, 140.0, 160.0, 160.0],
                         "Aggregates (kg)": [3037.08, 3032.71, 3007.92, 3003.54, 2756.67, 2751.67, 2723.33, 2718.33,
                                             3912.08, 3907.71, 3882.92, 3878.54, 3756.67, 3751.67, 3723.33, 3718.33],
                         "Admixture (kg)": [7.0, 10.5, 7.0, 10.5, 8.0, 12.0, 8.0, 12.0, 7.0, 10.5, 7.0, 10.5, 8.0, 12.0,
                                            8.0, 12.0], "Materials": ["powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3",
                                                                      "powder 1, liquid 2, admixture 1, aggregate 3"],
                         "Prop1": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                         "Prop2": ["Other Category", "Other Category", "Other Category", "Other Category",
                                   "Other Category", "Other Category", "Other Category", "Other Category",
                                   "Other Category", "Other Category", "Other Category", "Other Category",
                                   "Other Category", "Other Category", "Other Category", "Other Category"],
                         "Prop3": ["Not a number 2", "Not a number 2", "Not a number 2", "Not a number 2",
                                   "Not a number 2", "Not a number 2", "Not a number 2", "Not a number 2",
                                   "Not a number 2", "Not a number 2", "Not a number 2", "Not a number 2",
                                   "Not a number 2", "Not a number 2", "Not a number 2", "Not a number 2"],
                         "Prop4": [12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, None, None, None, None, None, None,
                                   None,
                                   None],
                         "fe3_o2": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.3, 2.3, 2.3, 2.3, 2.3, 2.3, 2.3,
                                    2.3],
                         "al2_o3": [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, None, None, None, None, None, None, None,
                                    None],
                         "fine": [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                                  1.0],
                         "na2_si_o3": [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
                                       20.0, 20.0, 20.0],
                         "na2_si_o3_mol": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                                           4.0],
                         "na_o_h": [4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1],
                         "h2_o_mol": [11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0,
                                      11.0, 11.0, 11.0],
                         "fine_aggregates": [27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0, 27.0,
                                             27.0, 27.0, 27.0, 27.0],
                         "coarse_aggregates": [9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0,
                                               9.0, 9.0],
                         "fineness_modulus": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                                              5.0],
                         "water_absorption": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                                              10.0, 10.0, 10.0, 10.0],
                         "total costs": [23.4, 23.44, 23.47, 23.5, 24.14, 24.18, 24.22, 24.26, 18.92, 18.94, 18.95,
                                         18.98, 18.74, 18.77, 18.78, 18.81],
                         "total co2_footprint": [62.82, 62.76, 62.49, 62.43, 61.26, 61.19, 60.86, 60.79, 62.81, 62.76,
                                                 62.55, 62.51, 61.62, 61.56, 61.31, 61.26],
                         "total delivery_time": [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
                         "total recycling_rate": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                  0.0, 0.0],
                         "total specific_gravity": [2.27, 2.27, 2.26, 2.27, 2.28, 2.28, 2.28, 2.28, 2.0, 2.0, 2.0, 2.0,
                                                    1.97, 1.97, 1.97, 1.97]})


def _create_expected_binder_df():
    return pd.DataFrame({"Idx_Sample": [0, 1, 2, 3, 4, 5, 6, 7],
                         "Powder (kg)": [109.49, 108.7, 105.63, 104.9, 72.99, 72.46, 70.42, 69.93],
                         "Liquid (kg)": [38.32, 38.05, 42.25, 41.96, 25.55, 25.36, 28.17, 27.97],
                         "Aggregates (kg)": [350.0, 350.0, 350.0, 350.0, 400.0, 400.0, 400.0, 400.0],
                         "Admixture (kg)": [2.19, 3.26, 2.11, 3.15, 1.46, 2.17, 1.41, 2.1],
                         "Materials": ["powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1",
                                       "powder 3, liquid 2, admixture 1, aggregate 1"],
                         "Prop1": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                         "Prop2": ["Category", "Category", "Category", "Category", "Category", "Category", "Category",
                                   "Category"],
                         "Prop3": ["Not a number 1", "Not a number 1", "Not a number 1", "Not a number 1",
                                   "Not a number 1", "Not a number 1", "Not a number 1", "Not a number 1"],
                         "Prop4": [10.2, 10.2, 10.2, 10.2, 10.2, 10.2, 10.2, 10.2],
                         "fe3_o2": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                         "al2_o3": [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
                         "fine": [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0],
                         "na2_si_o3": [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                         "na2_si_o3_mol": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
                         "na_o_h": [4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1],
                         "h2_o_mol": [11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0],
                         "fine_aggregates": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                         "coarse_aggregates": [4.4, 4.4, 4.4, 4.4, 4.4, 4.4, 4.4, 4.4],
                         "fineness_modulus": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                         "water_absorption": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                         "total costs": [48.49, 48.51, 48.33, 48.35, 48.99, 49.01, 48.89, 48.9],
                         "total co2_footprint": [19.19, 19.18, 19.12, 19.1, 19.46, 19.45, 19.41, 19.4],
                         "total delivery_time": [40, 40, 40, 40, 40, 40, 40, 40],
                         "total recycling_rate": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                         "total specific_gravity": [2.74, 2.74, 2.73, 2.73, 2.71, 2.71, 2.7, 2.7]})

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
