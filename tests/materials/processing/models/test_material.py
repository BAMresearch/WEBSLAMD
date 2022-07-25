from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Material, Costs


def test_material_constructor_sets_default_values():
    material = Material()

    assert material.name == ''
    assert material.type == ''
    assert material.costs is None
    assert material.additional_properties is None
    assert material.is_blended is False
    assert material.blending_ratios == ''
    assert material.created_from is None


def test_material_constructor_sets_properties():
    costs = Costs()
    material = Material(
        name='test material',
        type='Material',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        is_blended=True
    )

    assert material.name == 'test material'
    assert material.type == 'Material'
    assert material.costs == costs
    assert len(material.additional_properties) == 1
    assert material.is_blended is True


def test_material_constructor_generates_uuid():
    material = Material()

    assert material.uuid is not None


def test_material_constructor_generates_different_uuids():
    material_1 = Material()
    material_2 = Material()
    # This test may fail with an extremely low probability
    assert material_1.uuid != material_2.uuid


def test_material_costs_constructor_sets_default_values():
    costs = Costs()

    assert costs.delivery_time is None
    assert costs.costs is None
    assert costs.co2_footprint is None


def test_material_costs_constructor_sets_properties():
    costs = Costs(
        delivery_time=12.3,
        costs=45.6,
        co2_footprint=78.9
    )

    assert costs.delivery_time == 12.3
    assert costs.costs == 45.6
    assert costs.co2_footprint == 78.9
