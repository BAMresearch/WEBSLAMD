from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.material import Costs


def test_admixture_constructor_sets_default_values():
    admixture = Admixture()

    assert admixture.name == ''
    assert admixture.type == ''
    assert admixture.costs is None
    assert admixture.additional_properties is None


def test_admixture_constructor_sets_properties():
    costs = Costs()
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
    )

    assert admixture.name == 'test admixture'
    assert admixture.type == 'Admixture'
    assert admixture.costs == costs
    assert len(admixture.additional_properties) == 1
