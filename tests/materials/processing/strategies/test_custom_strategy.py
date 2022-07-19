from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy


def test_gather_composition_properties_adds_all_properties():
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=Costs(),
        additional_properties=[],
        custom_name='test custom name',
        custom_value='test custom value'
    )

    result = CustomStrategy.gather_composition_information(custom)
    assert result == ['Name: test custom name, ', 'Value: test custom value, ']
