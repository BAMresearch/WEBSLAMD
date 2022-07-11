from slamd.materials.processing.models.process import Process
from slamd.materials.processing.models.material import Costs


def test_process_constructor_sets_default_values():
    process = Process()

    assert process.name == ''
    assert process.type == ''
    assert process.costs == None
    assert process.additional_properties == None
    assert process.duration == None
    assert process.temperature == None
    assert process.relative_humidity == None


def test_process_constructor_sets_properties():
    costs = Costs()
    process = Process(
        name='test process',
        type='Process',
        costs=costs,
        additional_properties='name: test property, value: test value',
        duration=3.21,
        temperature=6.54,
        relative_humidity=9.87,
    )

    assert process.name == 'test process'
    assert process.type == 'Process'
    assert process.costs == costs
    assert process.additional_properties == 'name: test property, value: test value'
    assert process.duration == 3.21
    assert process.temperature == 6.54
    assert process.relative_humidity == 9.87
