from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.material import Costs


def test_admixture_constructor_sets_default_values():
    admixture = Admixture()

    assert admixture.name == ''
    assert admixture.type == ''
    assert admixture.costs == None
    assert admixture.additional_properties == None
    assert admixture.composition == None
    assert admixture.admixture_type == None


def test_admixture_constructor_sets_properties():
    costs = Costs()
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=costs,
        additional_properties='name: test property, value: test value',
        composition=10.4,
        admixture_type='test type'
    )

    assert admixture.name == 'test admixture'
    assert admixture.type == 'Admixture'
    assert admixture.costs == costs
    assert admixture.additional_properties == 'name: test property, value: test value'
    assert admixture.composition == 10.4
    assert admixture.admixture_type == 'test type'
