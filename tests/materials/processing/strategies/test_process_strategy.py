from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test process'),
                                             ('material_type', 'Process'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('duration', '3.21'),
                                             ('temperature', '6.54'),
                                             ('relative_humidity', '9.87'),
                                             ('submit', 'Save material')])
    model = ProcessStrategy.create_model(submitted_material)
    assert model.name == 'test process'
    assert model.type == 'Process'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.duration == 3.21
    assert model.temperature == 6.54
    assert model.relative_humidity == 9.87


def test_gather_composition_properties_adds_all_properties():
    process = Process(
        name='test process',
        type='Process',
        costs=Costs(),
        additional_properties=[],
        duration=3.21,
        temperature=6.54,
        relative_humidity=9.87,
    )

    result = ProcessStrategy.gather_composition_information(process)
    assert result == ['Duration (days): 3.21, ',
                      'Temperature (°C): 6.54, ',
                      'Relative Humidity (%): 9.87, ']


def test_convert_to_multidict_adds_all_properties():
    process = Process(
        name='test process',
        type='Process',
        costs=Costs(),
        additional_properties=[],
        duration=3.21,
        temperature=6.54,
        relative_humidity=9.87,
    )

    multidict = ProcessStrategy.convert_to_multidict(process)
    assert multidict['material_name'] == 'test process'
    assert multidict['material_type'] == 'Process'
    assert multidict['duration'] == '3.21'
    assert multidict['temperature'] == '6.54'
    assert multidict['relative_humidity'] == '9.87'
