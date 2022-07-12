from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.material import Costs


def test_custom_constructor_sets_default_values():
    custom = Custom()

    assert custom.name == ''
    assert custom.type == ''
    assert custom.costs is None
    assert custom.additional_properties is None
    assert custom.custom_name is None
    assert custom.custom_value is None


def test_custom_constructor_sets_properties():
    costs = Costs()
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        custom_name='test custom name',
        custom_value='test custom value'
    )

    assert custom.name == 'test custom'
    assert custom.type == 'Custom'
    assert custom.costs == costs
    assert len(custom.additional_properties) == 1
    assert custom.custom_name == 'test custom name'
    assert custom.custom_value == 'test custom value'
