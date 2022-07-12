from slamd.materials.processing.models.additional_property import AdditionalProperty


def test_additional_property_constructor_sets_default_values():
    additional_property = AdditionalProperty()

    assert additional_property.name == ''
    assert additional_property.value == ''


def test_additional_property_constructor_sets_properties():
    additional_property = AdditionalProperty(
        name='test name', value='test value')

    assert additional_property.name == 'test name'
    assert additional_property.value == 'test value'
