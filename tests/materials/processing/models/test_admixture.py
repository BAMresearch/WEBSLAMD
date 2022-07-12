from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.material import Costs


def test_admixture_constructor_sets_default_values():
    admixture = Admixture()

    assert admixture.name == ''
    assert admixture.type == ''
    assert admixture.costs is None
    assert admixture.additional_properties is None
    assert admixture.composition is None
    assert admixture.admixture_type is None


def test_admixture_constructor_sets_properties():
    costs = Costs()
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        composition=10.4,
        admixture_type='test type'
    )

    assert admixture.name == 'test admixture'
    assert admixture.type == 'Admixture'
    assert admixture.costs == costs
    assert len(admixture.additional_properties) == 1
    assert admixture.composition == 10.4
    assert admixture.admixture_type == 'test type'
