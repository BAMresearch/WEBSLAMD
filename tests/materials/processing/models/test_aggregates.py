from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.models.material import Costs


def test_aggregates_constructor_sets_default_values():
    aggregates = Aggregates()

    assert aggregates.name == ''
    assert aggregates.type == ''
    assert aggregates.costs is None
    assert aggregates.additional_properties is None
    assert aggregates.composition is None


def test_aggregates_constructor_sets_properties():
    costs = Costs()
    composition = Composition()
    aggregates = Aggregates(
        name='test aggregates',
        type='Aggregates',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        composition=composition,
    )

    assert aggregates.name == 'test aggregates'
    assert aggregates.type == 'Aggregates'
    assert aggregates.costs == costs
    assert len(aggregates.additional_properties) == 1
    assert aggregates.composition == composition


def test_aggregates_composition_constructor_sets_default_values():
    composition = Composition()

    assert composition.fine_aggregates is None
    assert composition.coarse_aggregates is None


def test_aggregates_composition_constructor_sets_properties():
    composition = Composition(
        fine_aggregates=123.45,
        coarse_aggregates=67.890
    )

    assert composition.fine_aggregates == 123.45
    assert composition.coarse_aggregates == 67.890
