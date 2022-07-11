from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.models.material import Costs


def test_liquid_constructor_sets_default_values():
    liquid = Liquid()

    assert liquid.name == ''
    assert liquid.type == ''
    assert liquid.costs == None
    assert liquid.additional_properties == None
    assert liquid.composition == None


def test_liquid_constructor_sets_properties():
    costs = Costs()
    composition = Composition()
    liquid = Liquid(
        name='test liquid',
        type='Liquid',
        costs=costs,
        additional_properties='name: test property, value: test value',
        composition=composition,
    )

    assert liquid.name == 'test liquid'
    assert liquid.type == 'Liquid'
    assert liquid.costs == costs
    assert liquid.additional_properties == 'name: test property, value: test value'
    assert liquid.composition == composition


def test_liquid_composition_constructor_sets_default_values():
    composition = Composition()

    assert composition.na2_si_o3 == None
    assert composition.na_o_h == None
    assert composition.na2_si_o3_specific == None
    assert composition.na_o_h_specific == None
    assert composition.total == None
    assert composition.na2_o == None
    assert composition.si_o2 == None
    assert composition.h2_o == None
    assert composition.na2_o_dry == None
    assert composition.si_o2_dry == None
    assert composition.water == None
    assert composition.na_o_h_total == None


def test_liquid_composition_constructor_sets_properties():
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

    assert composition.na2_si_o3 == 12.3
    assert composition.na_o_h == 23.4
    assert composition.na2_si_o3_specific == 34.5
    assert composition.na_o_h_specific == 45.6
    assert composition.total == 56.7
    assert composition.na2_o == 67.8
    assert composition.si_o2 == 78.9
    assert composition.h2_o == 89.0
    assert composition.na2_o_dry == 0.98
    assert composition.si_o2_dry == 9.87
    assert composition.water == 8.76
    assert composition.na_o_h_total == 7.65
