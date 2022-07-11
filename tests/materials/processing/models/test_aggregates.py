from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.models.material import Costs


def test_aggregates_constructor_sets_default_values():
    aggregates = Aggregates()

    assert aggregates.name == ''
    assert aggregates.type == ''
    assert aggregates.costs == None
    assert aggregates.additional_properties == None
    assert aggregates.composition == None


def test_aggregates_constructor_sets_properties():
    costs = Costs()
    composition = Composition()
    aggregates = Aggregates(
        name='test aggregates',
        type='Aggregates',
        costs=costs,
        additional_properties='name: test property, value: test value',
        composition=composition,
    )

    assert aggregates.name == 'test aggregates'
    assert aggregates.type == 'Aggregates'
    assert aggregates.costs == costs
    assert aggregates.additional_properties == 'name: test property, value: test value'
    assert aggregates.composition == composition


def test_aggregates_composition_constructor_sets_default_values():
    composition = Composition()

    assert composition.fine_aggregates == None
    assert composition.coarse_aggregates == None
    assert composition.fa_density == None
    assert composition.ca_density == None


def test_aggregates_composition_constructor_sets_properties():
    composition = Composition(
        fine_aggregates=123.45,
        coarse_aggregates=67.890,
        fa_density='test FA density',
        ca_density='test CA density'
    )

    assert composition.fine_aggregates == 123.45
    assert composition.coarse_aggregates == 67.890
    assert composition.fa_density == 'test FA density'
    assert composition.ca_density == 'test CA density'
