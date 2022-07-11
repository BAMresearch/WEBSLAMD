from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.material import Costs


def test_custom_constructor_sets_default_values():
    custom = Custom()

    assert custom.name == ''
    assert custom.type == ''
    assert custom.costs == None
    assert custom.additional_properties == None
    assert custom.custom_name == None
    assert custom.custom_value == None


def test_custom_constructor_sets_properties():
    costs = Costs()
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=costs,
        additional_properties='name: test property, value: test value',
        custom_name='test custom name',
        custom_value='test custom value'
    )

    assert custom.name == 'test custom'
    assert custom.type == 'Custom'
    assert custom.costs == costs
    assert custom.additional_properties == 'name: test property, value: test value'
    assert custom.custom_name == 'test custom name'
    assert custom.custom_value == 'test custom value'
