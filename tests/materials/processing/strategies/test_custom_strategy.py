from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test custom'),
                                             ('material_type', 'Custom'),
                                             ('specific_gravity', 1.0),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('submit', 'Save material')])
    model = CustomStrategy.create_model(submitted_material)
    assert model.name == 'test custom'
    assert model.type == 'Custom'
    assert model.specific_gravity == 1.0
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77


def test_gather_composition_properties_adds_all_compositional_properties():
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=Costs(),
        additional_properties=[],
    )

    result = CustomStrategy.gather_composition_information(custom)
    assert result is None


def test_convert_to_multidict_adds_all_properties():
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=Costs(),
        additional_properties=[],
    )

    multidict = CustomStrategy.convert_to_multidict(custom)
    assert multidict['material_name'] == 'test custom'
    assert multidict['material_type'] == 'Custom'
