from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test liquid'),
                                             ('material_type', 'Liquid'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('na2_si_o3', '12.3'),
                                             ('na_o_h', '23.4'),
                                             ('na2_si_o3_specific', '34.5'),
                                             ('na_o_h_specific', '45.6'),
                                             ('total', '56.7'),
                                             ('na2_o', '67.8'),
                                             ('si_o2', '78.9'),
                                             ('h2_o', '89.0'),
                                             ('na2_o_dry', '0.98'),
                                             ('si_o2_dry', '9.87'),
                                             ('water', '8.76'),
                                             ('na_o_h_total', '7.65'),
                                             ('submit', 'Save material')])
    model = LiquidStrategy.create_model(submitted_material)
    assert model.name == 'test liquid'
    assert model.type == 'Liquid'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.composition.na2_si_o3 == 12.3
    assert model.composition.na_o_h == 23.4
    assert model.composition.na2_si_o3_specific == 34.5
    assert model.composition.na_o_h_specific == 45.6
    assert model.composition.total == 56.7
    assert model.composition.na2_o == 67.8
    assert model.composition.si_o2 == 78.9
    assert model.composition.h2_o == 89.0
    assert model.composition.na2_o_dry == 0.98
    assert model.composition.si_o2_dry == 9.87
    assert model.composition.water == 8.76
    assert model.composition.na_o_h_total == 7.65


def test_gather_composition_properties_adds_all_properties():
    composition = Composition(
        na2_si_o3=12.3,
        na_o_h=23.4,
        na2_si_o3_specific=34.5,
        na_o_h_specific=45.6,
        total=56.7,
        na2_o=67.8,
        si_o2=78.9,
        h2_o=89.0,
        na2_o_dry=0.98,
        si_o2_dry=9.87,
        water=8.76,
        na_o_h_total=7.65
    )
    liquid = Liquid(
        name='test liquid',
        type='Liquid',
        costs=Costs(),
        additional_properties=[],
        composition=composition
    )

    result = LiquidStrategy.gather_composition_information(liquid)
    assert result == ['Na₂SiO₃: 12.3, ',
                      'NaOH: 23.4, ',
                      'Na₂SiO₃ specific: 34.5, ',
                      'NaOH specific: 45.6, ',
                      'Total solution: 56.7, ',
                      'Na₂O: 67.8, ',
                      'SiO₂: 78.9, ',
                      'H₂O: 89.0, ',
                      'Na₂O: 0.98, ',
                      'SiO₂: 9.87, ',
                      'Water: 8.76, ',
                      'Total NaOH: 7.65, ']
