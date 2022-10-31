from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.powder import Powder, Structure, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test powder'),
                                             ('material_type', 'Powder'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('fe3_o2', '12.3'),
                                             ('si_o2', '23.4'),
                                             ('al2_o3', '34.5'),
                                             ('ca_o', '45.6'),
                                             ('mg_o', '56.7'),
                                             ('na2_o', '67.8'),
                                             ('k2_o', '78.9'),
                                             ('s_o3', '89.0'),
                                             ('p2_o5', '0.98'),
                                             ('ti_o2', '9.87'),
                                             ('sr_o', '8.76'),
                                             ('mn2_o3', '7.65'),
                                             ('loi', '7.65'),
                                             ('fine', '123.45'),
                                             ('gravity', '678.90'),
                                             ('submit', 'Save material')])
    model = PowderStrategy.create_model(submitted_material)
    assert model.name == 'test powder'
    assert model.type == 'Powder'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.composition.fe3_o2 == 12.3
    assert model.composition.si_o2 == 23.4
    assert model.composition.al2_o3 == 34.5
    assert model.composition.ca_o == 45.6
    assert model.composition.mg_o == 56.7
    assert model.composition.na2_o == 67.8
    assert model.composition.k2_o == 78.9
    assert model.composition.s_o3 == 89.0
    assert model.composition.p2_o5 == 0.98
    assert model.composition.ti_o2 == 9.87
    assert model.composition.sr_o == 8.76
    assert model.composition.mn2_o3 == 7.65
    assert model.composition.loi == 7.65
    assert model.structure.fine == 123.45
    assert model.structure.gravity == 678.90


def test_gather_composition_properties_adds_all_properties():
    composition = Composition(
        fe3_o2=12.3,
        si_o2=23.4,
        al2_o3=34.5,
        ca_o=45.6,
        mg_o=56.7,
        na2_o=67.8,
        k2_o=78.9,
        s_o3=89.0,
        ti_o2=0.98,
        p2_o5=9.87,
        sr_o=8.76,
        mn2_o3=7.65,
        loi=2
    )
    structure = Structure(
        fine=123.45,
        gravity=678.90
    )
    powder = Powder(
        name='test powder',
        type='Powder',
        costs=Costs(),
        additional_properties=[],
        composition=composition,
        structure=structure
    )

    result = PowderStrategy.gather_composition_information(powder)
    assert result == ['Fe₂O₃ (m%): 12.3, ',
                      'SiO₂ (m%): 23.4, ',
                      'Al₂O₃ (m%): 34.5, ',
                      'CaO (m%): 45.6, ',
                      'MgO (m%): 56.7, ',
                      'Na₂O (m%): 67.8, ',
                      'K₂O (m%): 78.9, ',
                      'SO₃ (m%): 89.0, ',
                      'TiO₂ (m%): 0.98, ',
                      'P₂O₅ (m%): 9.87, ',
                      'SrO (m%): 8.76, ',
                      'Mn₂O₃ (m%): 7.65, ',
                      'LOI (m%): 2, ',
                      'Fine modules (m²/ton): 123.45, ',
                      'Specific gravity (m%): 678.9, ']


def test_convert_to_multidict_adds_all_properties():
    composition = Composition(
        fe3_o2=12.3,
        si_o2=23.4,
        al2_o3=34.5,
        ca_o=45.6,
        mg_o=56.7,
        na2_o=67.8,
        k2_o=78.9,
        s_o3=89.0,
        ti_o2=0.98,
        p2_o5=9.87,
        sr_o=8.76,
        mn2_o3=7.65,
        loi=7.65
    )
    structure = Structure(
        fine=123.45,
        gravity=678.90
    )
    powder = Powder(
        name='test powder',
        type='Powder',
        costs=Costs(),
        additional_properties=[],
        composition=composition,
        structure=structure
    )

    multidict = PowderStrategy.convert_to_multidict(powder)
    assert multidict['material_name'] == 'test powder'
    assert multidict['material_type'] == 'Powder'
    assert multidict['fe3_o2'] == '12.3'
    assert multidict['si_o2'] == '23.4'
    assert multidict['al2_o3'] == '34.5'
    assert multidict['ca_o'] == '45.6'
    assert multidict['mg_o'] == '56.7'
    assert multidict['na2_o'] == '67.8'
    assert multidict['k2_o'] == '78.9'
    assert multidict['s_o3'] == '89.0'
    assert multidict['ti_o2'] == '0.98'
    assert multidict['p2_o5'] == '9.87'
    assert multidict['sr_o'] == '8.76'
    assert multidict['mn2_o3'] == '7.65'
    assert multidict['loi'] == '7.65'
    assert multidict['fine'] == '123.45'
    assert multidict['gravity'] == '678.9'


def test_check_completeness_of_base_material_properties_returns_true_when_all_properties_are_incomplete(monkeypatch):
    def mock_is_complete(materials_as_dict, key1, key2):
        return True

    def mock_additional_properties_are_complete(model):
        return True

    monkeypatch.setattr(PropertyCompletenessChecker, 'is_complete', mock_is_complete)
    monkeypatch.setattr(PropertyCompletenessChecker, 'additional_properties_are_complete',
                        mock_additional_properties_are_complete)

    # We mock away all details in the test. Thus, we do not care about the actual input and simply use []
    complete = PowderStrategy.check_completeness_of_base_material_properties([])
    assert complete is True


def test_check_completeness_of_base_material_properties_returns_false_when_one_property_is_incomplete(monkeypatch):
    def mock_is_complete(materials_as_dict, key1, key2):
        if key1 == 'composition' and key2 == 'fe3_o2':
            return False
        return True

    def mock_additional_properties_are_complete(model):
        return True

    monkeypatch.setattr(PropertyCompletenessChecker, 'is_complete', mock_is_complete)
    monkeypatch.setattr(PropertyCompletenessChecker, 'additional_properties_are_complete',
                        mock_additional_properties_are_complete)

    # We mock away all details in the test. Thus, we do not care about the actual input and simply use []
    complete = PowderStrategy.check_completeness_of_base_material_properties([])

    assert complete is False


def test_check_completeness_of_base_material_properties_returns_false_when_additional_properties_are_incomplete(
        monkeypatch):
    def mock_is_complete(materials_as_dict, key1, key2):
        return True

    def mock_additional_properties_are_complete(model):
        return False

    monkeypatch.setattr(PropertyCompletenessChecker, 'is_complete', mock_is_complete)
    monkeypatch.setattr(PropertyCompletenessChecker, 'additional_properties_are_complete',
                        mock_additional_properties_are_complete)

    # We mock away all details in the test. Thus, we do not care about the actual input and simply use []
    complete = PowderStrategy.check_completeness_of_base_material_properties([])

    assert complete is False
