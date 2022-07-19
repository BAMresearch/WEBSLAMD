from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy


def test_gather_composition_properties_adds_all_properties():
    composition = Composition(
        fine_aggregates=123.45,
        coarse_aggregates=67.890,
        fa_density='test FA density',
        ca_density='test CA density'
    )
    aggregates = Aggregates(
        name='test aggregates',
        type='Aggregates',
        costs=Costs(),
        additional_properties=[],
        composition=composition,
    )

    result = AggregatesStrategy.gather_composition_information(aggregates)
    assert result == ['Fine Aggregates: 123.45, ',
                      'Coarse Aggregates: 67.89, ',
                      'FA Density: test FA density, ',
                      'CA Density: test CA density, ']
