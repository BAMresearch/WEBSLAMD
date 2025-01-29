from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test liquid'),
                                             ('material_type', 'Liquid'),
                                             ('specific_gravity', 1.0),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('na2_si_o3', '12.3'),
                                             ('na_o_h', '23.4'),
                                             ('na2_si_o3_mol', '34.5'),
                                             ('na_o_h_mol', '45.6'),
                                             ('na2_o', '67.8'),
                                             ('si_o2', '78.9'),
                                             ('h2_o', '89.0'),
                                             ('na2_o_mol', '0.98'),
                                             ('si_o2_mol', '9.87'),
                                             ('h2_o_mol', '8.76'),
                                             ('submit', 'Save material')])
    model = LiquidStrategy.create_model(submitted_material)
    assert model.name == 'test liquid'
    assert model.type == 'Liquid'
    assert model.specific_gravity == 1.0
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.composition.na2_si_o3 == 12.3
    assert model.composition.na_o_h == 23.4
    assert model.composition.na2_si_o3_mol == 34.5
    assert model.composition.na_o_h_mol == 45.6
    assert model.composition.na2_o == 67.8
    assert model.composition.si_o2 == 78.9
    assert model.composition.h2_o == 89.0
    assert model.composition.na2_o_mol == 0.98
    assert model.composition.si_o2_mol == 9.87
    assert model.composition.h2_o_mol == 8.76


def test_gather_composition_properties_adds_all_properties():
    composition = Composition(
        na2_si_o3=12.3,
        na2_si_o3_mol=34.5,
        na_o_h=23.4,
        na_o_h_mol=45.6,
        na2_o=67.8,
        na2_o_mol=0.98,
        si_o2=78.9,
        si_o2_mol=9.87,
        h2_o=89.0,
        h2_o_mol=8.76,
    )
    liquid = Liquid(
        name='test liquid',
        type='Liquid',
        costs=Costs(),
        additional_properties=[],
        composition=composition
    )

    result = LiquidStrategy.gather_composition_information(liquid)
    assert result == ['Na₂SiO₃ (m%): 12.3, ',
                      'Na₂SiO₃ (mol%): 34.5, ',
                      'NaOH (m%): 23.4, ',
                      'NaOH (mol%): 45.6, ',
                      'Na₂O (m%): 67.8, ',
                      'Na₂O (mol%): 0.98, ',
                      'SiO₂ (m%): 78.9, ',
                      'SiO₂ (mol%): 9.87, ',
                      'H₂O (m%): 89.0, ',
                      'H₂O (mol%): 8.76, ']


def test_convert_to_multidict_adds_all_properties():
    composition = Composition(
        na2_si_o3=12.3,
        na_o_h=23.4,
        na2_si_o3_mol=34.5,
        na_o_h_mol=45.6,
        na2_o=67.8,
        si_o2=78.9,
        h2_o=89.0,
        na2_o_mol=0.98,
        si_o2_mol=9.87,
        h2_o_mol=8.76,
    )
    liquid = Liquid(
        name='test liquid',
        type='Liquid',
        costs=Costs(),
        additional_properties=[],
        composition=composition
    )

    multidict = LiquidStrategy.convert_to_multidict(liquid)
    assert multidict['material_name'] == 'test liquid'
    assert multidict['material_type'] == 'Liquid'
    assert multidict['na2_si_o3'] == '12.3'
    assert multidict['na_o_h'] == '23.4'
    assert multidict['na2_si_o3_mol'] == '34.5'
    assert multidict['na_o_h_mol'] == '45.6'
    assert multidict['na2_o'] == '67.8'
    assert multidict['si_o2'] == '78.9'
    assert multidict['h2_o'] == '89.0'
    assert multidict['na2_o_mol'] == '0.98'
    assert multidict['si_o2_mol'] == '9.87'
    assert multidict['h2_o_mol'] == '8.76'
