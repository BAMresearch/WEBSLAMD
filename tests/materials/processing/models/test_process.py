from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.models.material import Costs


def test_process_constructor_sets_default_values():
    process = Process()

    assert process.name == ''
    assert process.type == ''
    assert process.costs is None
    assert process.additional_properties is None
    assert process.duration is None
    assert process.temperature is None
    assert process.relative_humidity is None


def test_process_constructor_sets_properties():
    costs = Costs()
    process = Process(
        name='test process',
        type='Process',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        duration=3.21,
        temperature=6.54,
        relative_humidity=9.87,
    )

    assert process.name == 'test process'
    assert process.type == 'Process'
    assert process.costs == costs
    assert len(process.additional_properties) == 1
    assert process.duration == 3.21
    assert process.temperature == 6.54
    assert process.relative_humidity == 9.87
