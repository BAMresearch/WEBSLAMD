from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test aggregates'),
                                             ('material_type', 'Aggregates'),
                                             ('specific_gravity', '2.40'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('fine_aggregates', '123.45'),
                                             ('coarse_aggregates', '67.890'),
                                             ('fineness_modulus', '500'),
                                             ('water_absorption', '400'),
                                             ('submit', 'Save material')])
    model = AggregatesStrategy.create_model(submitted_material)
    assert model.name == 'test aggregates'
    assert model.type == 'Aggregates'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.composition.fine_aggregates == 123.45
    assert model.composition.coarse_aggregates == 67.890
    assert model.composition.fineness_modulus == 500
    assert model.composition.water_absorption == 400


def test_gather_composition_properties_adds_all_properties():
    composition = Composition(
        fine_aggregates=123.45,
        coarse_aggregates=67.890,
        fineness_modulus=123.45,
        water_absorption=543.21
    )
    aggregates = Aggregates(
        name='test aggregates',
        type='Aggregates',
        costs=Costs(),
        additional_properties=[],
        composition=composition,
    )

    result = AggregatesStrategy.gather_composition_information(aggregates)
    assert result == ['Fine Aggregates (m%): 123.45, ',
                      'Coarse Aggregates (m%): 67.89, ',
                      'Fineness modulus (m³/kg): 123.45, ',
                      'Water absorption (m%): 543.21, ']


def test_convert_to_multidict_adds_all_properties():
    composition = Composition(
        fine_aggregates=123.45,
        coarse_aggregates=67.890,
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
