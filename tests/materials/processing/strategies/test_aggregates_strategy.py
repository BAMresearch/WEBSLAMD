from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test aggregates'),
                                             ('material_type', 'Aggregates'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('fine_aggregates', '123.45'),
                                             ('coarse_aggregates', '67.890'),
                                             ('fa_density', 'test FA density'),
                                             ('ca_density', 'test CA density'),
                                             ('submit', 'Save material')])
    model = AggregatesStrategy.create_model(submitted_material)
    assert model.name == 'test aggregates'
    assert model.type == 'Aggregates'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.composition.fine_aggregates == 123.45
    assert model.composition.coarse_aggregates == 67.890
    assert model.composition.fa_density == 'test FA density'
    assert model.composition.ca_density == 'test CA density'


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


def test_convert_to_multidict_adds_all_properties():
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

    multidict = AggregatesStrategy.convert_to_multidict(aggregates)
    assert multidict['material_name'] == 'test aggregates'
    assert multidict['material_type'] == 'Aggregates'
    assert multidict['fine_aggregates'] == '123.45'
    assert multidict['coarse_aggregates'] == '67.89'
    assert multidict['fa_density'] == 'test FA density'
    assert multidict['ca_density'] == 'test CA density'
