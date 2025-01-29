from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.admixture_strategy import AdmixtureStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test admixture'),
                                             ('material_type', 'Admixture'),
                                             ('specific_gravity', '1.10'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('submit', 'Save material')])
    model = AdmixtureStrategy.create_model(submitted_material)
    assert model.name == 'test admixture'
    assert model.type == 'Admixture'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77


def test_gather_composition_properties_adds_all_properties():
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=Costs(),
        additional_properties=[],
    )

    result = AdmixtureStrategy.gather_composition_information(admixture)
    assert result is None


def test_convert_to_multidict_adds_all_properties():
    admixture = Admixture(
        name='test admixture',
        type='Admixture',
        costs=Costs(),
        additional_properties=[],
    )

    multidict = AdmixtureStrategy.convert_to_multidict(admixture)
    assert multidict['material_name'] == 'test admixture'
    assert multidict['material_type'] == 'Admixture'
