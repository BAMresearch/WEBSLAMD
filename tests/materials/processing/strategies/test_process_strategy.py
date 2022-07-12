from slamd.materials.processing.models.process import Process
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy


def test_gather_composition_properties_adds_all_properties():
    strategy = ProcessStrategy()
    process = Process(
        name='test process',
        type='Process',
        costs=Costs(),
        additional_properties=[],
        duration=3.21,
        temperature=6.54,
        relative_humidity=9.87,
    )
    
    result = strategy.gather_composition_information(process)
    assert result == ['Duration: 3.21, ',
                      'Temperature: 6.54, ', 'Relative Humidity: 9.87, ']
