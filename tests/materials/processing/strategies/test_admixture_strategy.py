from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.admixture_strategy import AdmixtureStrategy


def test_gather_composition_properties_adds_all_properties():
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=Costs(),
        additional_properties=[],
        composition=10.4,
        admixture_type='test type'
    )

    result = AdmixtureStrategy.gather_composition_information(admixture)
    assert result == ['Composition: 10.4, ', 'Type: test type, ']
